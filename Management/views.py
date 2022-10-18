from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import LoginForm, NewTestForm
from django.contrib.auth import (
    authenticate,
    login as system_login,
    logout as system_logout,
)
from .models import SubjectiveTest, Sample, Question
import zipfile
import uuid
import os
import json
from SubjectiveTestSystem.settings import MEDIA_ROOT
from django.core.files import File
from pathlib import Path
from django.db import transaction
import shutil
from User.models import Answer

# Create your views here.

login_url = "/management/login/"


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                password = login_form.cleaned_data["password"]
                username = login_form.cleaned_data["username"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    system_login(request, user)
                    return HttpResponseRedirect(reverse("Management:index"))
                else:
                    login_form.add_error("password", "Wrong password or username!")
        else:
            login_form = LoginForm()
        return render(request, "Management/login.html", {"form": login_form})
    return HttpResponseRedirect(reverse("Management:index"))


@login_required(login_url=login_url)
def index(request):
    all_tests = SubjectiveTest.objects.all()
    return render(request, "Management/index.html", context={"all_tests": all_tests})


@login_required(login_url=login_url)
def view(request, subjective_test_id):
    subjective_test = get_object_or_404(SubjectiveTest, pk=subjective_test_id)
    return render(
        request, "Management/view.html", context={"subjective_test": subjective_test}
    )


@login_required(login_url=login_url)
def export(request, subjective_test_id):
    subjective_test = get_object_or_404(SubjectiveTest, pk=subjective_test_id)
    # SubjectiveTest -> Question -> Sample -> User -> Answer
    # abx: answer.answer是sample id
    # mos: answer.answer是给定的sample的mos得分
    # cmos: answer.answer是给定的sample的CMOS得分
    response = []
    for question in subjective_test.question_set.all():
        type = question.get_current_question_type_str()
        q = {}
        if type== 'ABX':
            answers = Answer.objects.all().filter(subjective_test_id__exact=subjective_test_id,question_id__exact=question.id)
            q['type'] = 'ABX'
            q['ans'] = []
            for answer in answers:
                sample = Sample.objects.get(id__exact=answer.answer)
                q['ans'].append({'name':sample.original_name,'user':answer.user.username})
            response.append(q)
        elif type=='MOS':
            q['type'] = "MOS"
            q['ans'] = []
            for sample in question.sample_set.all():
                if sample.score:
                    answers = Answer.objects.all().filter(subjective_test_id__exact=subjective_test_id,question_id__exact=question.id,
                    sample_id__exact=sample.id)
                    qs = {'sample_name':sample.original_name,'ans':[]}
                    for answer in answers:
                        qs['ans'].append({'user':answer.user.username,'score':answer.answer})
                    q['ans'].append(qs)
            response.append(q)
        elif type=='CMOS':
            q['type'] = 'CMOS'
            q['ans'] = []
            for sample in question.sample_set.all():
                if sample.score:
                    answers = Answer.objects.all().filter(subjective_test_id__exact=subjective_test_id,question_id__exact=question.id,
                    sample_id__exact=sample.id)
                    qs = {'sample_name':sample.original_name,'ans':[]}
                    for answer in answers:
                        qs['ans'].append({'user':answer.user.username,'score':answer.answer})
                    q['ans'].append(qs)
            response.append(q)
    return JsonResponse(response,safe=False)


CONFIG_FILENAME = "config.json"


@login_required(login_url=login_url)
def new(request):
    if request.method == "POST":
        form = NewTestForm(request.POST, request.FILES)
        if form.is_valid:
            file = request.FILES["file"]
            destination_dir_name = uuid.uuid4().hex
            destination_dir_path = os.path.join(MEDIA_ROOT, destination_dir_name)
            destination_name = destination_dir_path + ".zip"
            with open(destination_name, "wb") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            zip_file = zipfile.ZipFile(destination_name, "r", allowZip64=True)
            if CONFIG_FILENAME in zip_file.namelist():
                zip_file.extractall(destination_dir_path)
                zip_file.close()
                with open(os.path.join(destination_dir_path, CONFIG_FILENAME)) as f:
                    configuration_json = json.load(f)
                try:
                    with transaction.atomic():
                        subjective_test = SubjectiveTest(
                            name=request.POST["name"], enable=True
                        )
                        subjective_test.save()
                        for question_conf in configuration_json:
                            question = Question(
                                subjective_test=subjective_test,
                                type=Question.str_to_question_type(
                                    question_conf["type"]
                                ),
                                text=question_conf["text"],
                            )
                            question.save()
                            for sample_conf in question_conf["samples"]:
                                path = Path(
                                    os.path.join(
                                        destination_dir_path, sample_conf["path"]
                                    )
                                )
                                with path.open(mode="rb") as f:
                                    sample = Sample(
                                        question=question,
                                        type=Sample.str_to_sample_type(
                                            sample_conf["type"]
                                        ),
                                        file_type=Sample.str_to_sample_file_type(
                                            sample_conf["file_type"]
                                        ),
                                        score=sample_conf["score"],
                                        text=sample_conf["text"],
                                        file=File(f, name=path.name),
                                        original_name=path.name,
                                    )
                                    sample.save()
                except:
                    os.removedirs(destination_dir_path)
                    os.remove(destination_name)
                    form.add_error("file", "create new subjective test error!")
                else:
                    shutil.rmtree(destination_dir_path)
                    os.remove(destination_name)
                    return HttpResponseRedirect(reverse("Management:index"))
            else:
                form.add_error("file", f"can't find {CONFIG_FILENAME} in zip file!")

    else:
        form = NewTestForm()
    return render(request, "Management/new.html", context={"form": form})


@login_required(login_url=login_url)
def delete(request, subjective_test_id):
    SubjectiveTest.objects.filter(id=subjective_test_id).delete()
    return HttpResponseRedirect(reverse("Management:index"))


@login_required(login_url=login_url)
def enable(request, subjective_test_id):
    subjective_test = get_object_or_404(SubjectiveTest, pk=subjective_test_id)
    subjective_test.enable = not subjective_test.enable
    subjective_test.save()
    return HttpResponseRedirect(reverse("Management:index"))


def logout(request):
    system_logout(request)
    return HttpResponseRedirect(reverse("Management:login"))
