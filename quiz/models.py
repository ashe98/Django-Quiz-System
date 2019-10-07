from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Questions(models.Model):
    question = models.CharField(max_length = 250)
    optiona = models.CharField(max_length = 100)
    optionb = models.CharField(max_length = 100)
    optionc = models.CharField(max_length = 100)
    optiond = models.CharField(max_length = 100)
    answer = models.CharField(max_length = 100)
    marks = models.IntegerField(default=1)
    #catagory = models.CharField(max_length=20, choices = CAT_CHOICES)

    class Meta:
        ordering = ('-question',)

    def __str__(self):
        return self.question

class Quiz(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    @property
    def getusername(self):
        return self.created_by.username

    quiz_name = models.CharField(max_length = 100)
    qs = models.ManyToManyField(Questions)

    class Meta:
        ordering = ('-quiz_name',)

    def __str__(self):
        return self.quiz_name

class Scores(models.Model):
    noq = models.ForeignKey(Quiz, null = True, on_delete=models.PROTECT)

    @property
    def quizname(self):
        return self.noq.quiz_name

    test_taker = models.ForeignKey(User, null = True, on_delete=models.PROTECT)

    @property
    def getusername(self):
        return self.test_taker.username
    
    scoreofu = models.IntegerField(default=0)
