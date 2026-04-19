from django.db import models
from django.contrib.auth.models import User

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Learner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Course(models.Model):
    name = models.CharField(max_length=200)

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def is_get_score(self, selected_ids):
        correct_choices = self.choice_set.filter(is_correct=True)
        if set(selected_ids) == set([c.id for c in correct_choices]):
            return 1
        return 0

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)