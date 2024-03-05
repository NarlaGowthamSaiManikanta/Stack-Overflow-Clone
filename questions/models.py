from django.db import models
from user.models import User
from django.core.validators import MinLengthValidator


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(validators=[MinLengthValidator(220,
                                                              'Body requires minimum 220 characters.')])
    posted_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    bounty_amount = models.IntegerField(default=0)
    saved_by = models.ManyToManyField(User, related_name='question_save', blank=True)
    up_votes = models.ManyToManyField(User, related_name='up_votes', blank=True)
    down_votes = models.ManyToManyField(User, related_name='down_votes', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"Question - {self.id}"

    def get_votes(self):
        return self.up_votes.count() - self.down_votes.count()


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(validators=[MinLengthValidator(220,
                                                              'Body requires minimum 220 characters.')])
    accepted_answer_for = models.OneToOneField(Question, on_delete=models.CASCADE, related_name='accepted_answer',
                                               null=True, blank=True)
    saved_by = models.ManyToManyField(User, related_name='answer_save', blank=True)
    up_votes = models.ManyToManyField(User, related_name='ans_up_votes', blank=True)
    down_votes = models.ManyToManyField(User, related_name='ans_down_votes', blank=True)

    def __str__(self):
        return f"Answer - {self.id} for question {self.question.id}"

    def get_votes(self):
        return self.up_votes.count() - self.down_votes.count()


class QuestionComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"QuestionComments - {self.id} for question {self.question.id} by {self.user.id}"


class AnswerComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"AnswerComments - {self.id} for answer {self.answer.id} by {self.user.id}"


class Visit(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question - {self.question.id} visited by {self.user.id}"
