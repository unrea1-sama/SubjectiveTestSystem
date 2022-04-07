from django.db import models

# Create your models here.


class SubjectiveTest(models.Model):
    name = models.CharField(max_length=300)
    enable = models.BooleanField(help_text='Whether this test are enabled')
    def __str__(self):
        return self.name


class Question(models.Model):
    subjective_test = models.ForeignKey(SubjectiveTest, on_delete=models.CASCADE)
    type = models.IntegerField(
        help_text="Type of question. 0 is ABX, 1 is MOS, 2 is CMOS."
    )
    text = models.CharField(max_length=10240, help_text="Description.", default="")

    @staticmethod
    def question_type_to_str(type):
        if type == 0:
            return "ABX"
        if type == 1:
            return "MOS"
        if type == 2:
            return "CMOS"

    @staticmethod
    def str_to_question_type(s):
        if s == "ABX":
            return 0
        if s == "MOS":
            return 1
        if s == "CMOS":
            return 2
    
    def get_current_question_type_str(self):
        return self.question_type_to_str(self.type)

    def __str__(self):
        return "{}:{}".format(Question.question_type_to_str(self.type), self.text)


class Sample(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    file = models.FileField(max_length=4096)
    type = models.IntegerField(
        help_text="Type of sample. 0 is ground truth, 1 is predicted sample."
    )
    file_type = models.IntegerField(
        help_text="File type of sample. 0 is audio, 1 is video."
    )
    score = models.BooleanField(help_text="Whether this sample is scored.", default=0)
    text = models.CharField(max_length=10240, help_text="Description.", default="")
    original_name = models.CharField(max_length=4096,help_text='Original filename.',default='')

    @staticmethod
    def sample_type_to_str(type):
        if type == 1:
            return "Predicted"
        if type == 0:
            return "Ground Truth"

    @staticmethod
    def str_to_sample_type(s):
        if s == "P":
            return 1
        if s == "G":
            return 0

    @staticmethod
    def str_to_sample_file_type(s):
        if s =='audio':
            return 0
        if s =='video':
            return 1

    def get_current_sample_type_str(self):
        return self.sample_type_to_str(self.type)

