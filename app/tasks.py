import datetime

from .models import ChoreAssignment, ChoreInstance, ChoreStatus
from django.contrib.auth.models import User


def mark_late_chores():
    now = datetime.datetime.now()
    for user in User.objects.all():
        instances = user.choreinstance_set.filter(status=ChoreStatus.ASSIGNED).all()
        for instance in instances:
            if now >= instance.due_date:
                instance.status = ChoreStatus.INCOMPLETE
                instance.save()
                # TODO email


def create_chore_instances():
    """
    Creates ChoreInstance objects up to a week ahead by cycling through users
    with assigned ChoreAssignments
    """
    for user in User.objects.all():
        assignments = user.choreassignment_set.all()
        for assignment in assignments:
            assigned_instance_count = assignment.choreinstance_set.filter(
                user=user, status=ChoreStatus.ASSIGNED
            ).count()

            if assigned_instance_count == 0:
                assignment.create_instance(user)


def update_chores():
    """
    Main function run as a recurring task.
    Runs all necessary chore checking and creation work.
    """
    # Marking late chores must happen before creating chores
    # or else new instances will not be created
    mark_late_chores()

    create_chore_instances()
