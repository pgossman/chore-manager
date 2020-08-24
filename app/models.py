from django.db import models
from django.contrib.auth.models import User


class Chore(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class ChoreStatus(models.TextChoices):
    ASSIGNED = "A"
    COMPLETE = "C"
    INCOMPLETE = "I"
    SUBMITTED = "S"


class ChoreInstance(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ChoreStatus.choices)
    due_date = models.DateTimeField()

    notes = models.CharField(max_length=5000, default="")

    def __str__(self):
        return f"{self.user.first_name} - {self.chore} - Due: {self.due_date}"


class Photo(models.Model):
    filename = models.CharField(max_length=2000)
    instance = models.ForeignKey(ChoreInstance, on_delete=models.CASCADE)

    def __str__(self):
        return filename
