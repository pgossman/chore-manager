from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ChoreStatus(models.TextChoices):
    ASSIGNED = "A", _("Assigned")
    COMPLETE = "C", _("Complete")
    INCOMPLETE = "I", _("Incomplete")
    SUBMITTED = "S", _("Submitted")


class PartOfDay(models.TextChoices):
    MORNING = "M", _("Morning")
    AFTERNOON = "A", _("Afternoon")
    EVENING = "E", _("Evening")
    ANY = "N", _("Any")


class DayOfWeek(models.TextChoices):
    MONDAY = "MO", _("Monday")
    TUESDAY = "TU", _("Tuesday")
    WEDNESDAY = "WE", _("Wednesday")
    THURSDAY = "TH", _("Thursday")
    FRIDAY = "FR", _("Friday")
    SATURDAY = "SA", _("Saturday")
    SUNDAY = "SU", _("Sunday")


class Chore(models.Model):
    """The template for any chore.

    Example: sweep kitchen floors
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ChoreAssignment(models.Model):
    """An assignment of a chore, containing an assigned chore,
    a user(s) it is assigned to, a day of week, and (optionally)
    a time of day

    Example: Sam will sweep kitchen floors on Monday mornings
    """

    users = models.ManyToManyField(User)
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)

    dow = models.CharField(max_length=2, choices=DayOfWeek.choices)
    time = models.CharField(max_length=1, choices=PartOfDay.choices)

    def __str__(self):
        if self.time == PartOfDay.ANY:
            time_str = ""
        else:
            time_str = f" {PartOfDay(self.time).label}"

        return f"{self.chore.name} {DayOfWeek(self.dow).label}{time_str}"


class ChoreInstance(models.Model):
    """A date-specific instance of a chore assignment.
    Tracks the completion status of the instance.

    Example: Sam will sweep kitchen floors on Monday, 8/1/1970,
             and it has been submitted for review.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    assignment = models.ForeignKey(ChoreAssignment, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ChoreStatus.choices)

    due_date = models.DateTimeField()
    submission_date = models.DateTimeField(default=None, null=True)

    notes = models.CharField(max_length=5000, default="")

    def __str__(self):
        return f"{self.user.first_name} - {self.assignment.chore.name} - Due: {self.due_date}"


class Photo(models.Model):
    filename = models.CharField(max_length=2000)
    instance = models.ForeignKey(ChoreInstance, on_delete=models.CASCADE)

    def __str__(self):
        return filename
