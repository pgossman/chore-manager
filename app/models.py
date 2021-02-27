import datetime
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
        return f"{DayOfWeek(self.dow).label} {PartOfDay(self.time).label} - {self.chore.name}"

    def create_instance(self, user):
        ChoreInstance.objects.create(
            user=user,
            assignment=self,
            status=ChoreStatus.ASSIGNED,
            due_date=self.next_due_date(),
        )

    def next_due_date(self):
        def to_weekday(dow):
            return {
                DayOfWeek.MONDAY: 0,
                DayOfWeek.TUESDAY: 1,
                DayOfWeek.WEDNESDAY: 2,
                DayOfWeek.THURSDAY: 3,
                DayOfWeek.FRIDAY: 4,
                DayOfWeek.SATURDAY: 5,
                DayOfWeek.SUNDAY: 6,
            }[dow]

        def to_time(time):
            return {
                PartOfDay.MORNING: datetime.timedelta(hours=16),
                PartOfDay.AFTERNOON: datetime.timedelta(hours=20),
                PartOfDay.EVENING: datetime.timedelta(hours=23, minutes=59),
                PartOfDay.ANY: datetime.timedelta(hours=23, minutes=59),
            }[time]

        result = datetime.datetime.now()

        # Set time
        result = result.replace(hour=0, minute=0, second=0, microsecond=0)
        result += to_time(self.time)

        # Set day to next weekday
        dow = to_weekday(self.dow)
        days_ahead = result.weekday() - dow
        if days_ahead < 0:
            days_ahead *= -1
        else:
            days_ahead = 7 - days_ahead
        result += datetime.timedelta(days=days_ahead)

        return result


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

    # Datetime that a user submits an instance for review to worms
    submission_date = models.DateTimeField(default=None, null=True, blank=True)

    # Notes from user made on submission
    notes = models.CharField(max_length=5000, default="", blank=True)

    def to_str(self, assignment=True, user=False):
        user_str = f"{self.user} - "
        name_str = f"{self.assignment.chore.name} - "
        assignment_str = f"{ChoreStatus(self.status).label} -"
        due_str = self.due_date.strftime("%m/%d/%Y %-I %p")
        due_str = f" Due: {due_str}"

        if user:
            name_str = user_str + name_str

        if assignment:
            return name_str + assignment_str + due_str
        else:
            return name_str + due_str

    def __str__(self):
        return self.to_str()


class Photo(models.Model):
    filename = models.CharField(max_length=2000)
    instance = models.ForeignKey(ChoreInstance, on_delete=models.CASCADE)

    def __str__(self):
        return filename
