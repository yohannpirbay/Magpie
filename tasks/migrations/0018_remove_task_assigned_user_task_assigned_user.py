# Generated by Django 4.2.6 on 2023-12-11 17:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_task_finished_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_user',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_user',
            field=models.ManyToManyField(related_name='tasks_assigned', to=settings.AUTH_USER_MODEL),
        ),
    ]