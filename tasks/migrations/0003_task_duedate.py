# Generated by Django 4.2.6 on 2023-11-14 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dueDate',
            field=models.DateField(default='2032-12-25'),
        ),
    ]
