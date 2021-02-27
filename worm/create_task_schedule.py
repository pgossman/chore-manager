# Run with "python manage.py shell < {this file}"

from django_q.models import Schedule

Schedule.objects.create(
    func="app.tasks.update_chores",
    schedule_type=Schedule.MINUTES,
    minutes=1,
    repeats=-1,
)
