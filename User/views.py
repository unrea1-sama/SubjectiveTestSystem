from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import (
    authenticate,
    login as system_login,
    logout as system_logout,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from Management.models import SubjectiveTest, Question, Sample
from .models import Answer
from django.db import transaction

# Create your views here.

login_url = "/user/login"

DEFAULT_PASSWORD = "1234567890"


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                user = authenticate(
                    request, username=username, password=DEFAULT_PASSWORD
                )
                if user is not None:
                    system_login(request, user)
                else:
                    new_user = User.objects.create_user(
                        username, "test@test.com", DEFAULT_PASSWORD
                    )
                    new_user.save()
                    user = authenticate(
                        request, username=username, password=DEFAULT_PASSWORD
                    )
                    system_login(request, user)
        else:
            login_form = LoginForm()
            return render(request, "User/login.html", {"form": login_form})
    return HttpResponseRedirect(reverse("User:index"))


@login_required(login_url=login_url)
def index(request):
    all_tests = SubjectiveTest.objects.filter(enable__exact=True)
    return render(request, "User/index.html", context={"all_tests": all_tests})


@login_required(login_url=login_url)
def view(request, subjective_test_id):
    subjective_test = get_object_or_404(SubjectiveTest, pk=subjective_test_id)
    if request.method == "POST":
        # try:
        with transaction.atomic():
            for key in request.POST:
                temp = key.split("-")
                if len(temp) == 3:
                    _, question_id, sample_id = temp
                    try:
                        question = Question.objects.get(id=question_id)
                        sample = Sample.objects.get(id=sample_id)
                        answer = Answer.objects.get(
                            user=request.user,
                            subjective_test_id__exact=subjective_test_id,
                            question_id__exact=question_id,
                            sample_id__exact=sample_id,
                        )
                    except Answer.DoesNotExist:
                        answer = Answer(
                            question_id=question_id,
                            sample_id=sample_id,
                            subjective_test_id=subjective_test_id,
                            user=request.user,
                        )
                    except (Sample.DoesNotExist, Question.DoesNotExist):
                        pass
                    answer.answer = request.POST[key]
                    answer.save()
                elif len(temp) == 2:
                    # abx: POST[key]是sample id
                    # mos: POST[key]是给定的sample的mos得分
                    # cmos: POST[key]是给定的一组sample的CMOS得分
                    _, question_id = temp
                    try:
                        question = Question.objects.get(id=question_id)
                        answer = Answer.objects.get(
                            user=request.user,
                            subjective_test_id__exact=subjective_test_id,
                            question_id__exact=question_id,
                            sample_id__exact=0,
                        )
                    except Answer.DoesNotExist:
                        answer = Answer(
                            question_id=question_id,
                            sample_id=0,
                            subjective_test_id=subjective_test_id,
                            user=request.user,
                        )
                    except (Sample.DoesNotExist, Question.DoesNotExist):
                        continue
                    answer.answer = request.POST[key]
                    answer.save()
                else:
                    continue
        # except:
        #    pass
    return render(
        request,
        "User/view.html",
        context={"subjective_test": subjective_test, "user": request.user},
    )


@login_required(login_url=login_url)
def delete(request, subjective_test_id):
    pass


def logout(request):
    system_logout(request)
    return HttpResponseRedirect(reverse("User:login"))
