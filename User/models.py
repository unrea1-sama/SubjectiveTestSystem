from django.db import models
from Management.models import Sample, Question, SubjectiveTest
from django.contrib.auth.models import User

# Create your models here.


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample_id = models.PositiveIntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    subjective_test = models.ForeignKey(SubjectiveTest, on_delete=models.CASCADE)
    answer = models.IntegerField()
