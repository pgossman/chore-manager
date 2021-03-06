# Generated by Django 3.1 on 2020-08-27 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ChoreAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dow', models.CharField(choices=[('MO', 'Monday'), ('TU', 'Tuesday'), ('WE', 'Wednesday'), ('TH', 'Thursday'), ('FR', 'Friday'), ('SA', 'Saturday'), ('SU', 'Sunday')], max_length=2)),
                ('time', models.CharField(choices=[('M', 'Morning'), ('A', 'Afternoon'), ('E', 'Evening'), ('N', 'Any')], max_length=1)),
                ('chore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.chore')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChoreInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Assigned'), ('C', 'Complete'), ('I', 'Incomplete'), ('S', 'Submitted')], max_length=1)),
                ('due_date', models.DateTimeField()),
                ('submission_date', models.DateTimeField(default=None, null=True)),
                ('notes', models.CharField(default='', max_length=5000)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.choreassignment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=2000)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.choreinstance')),
            ],
        ),
    ]
