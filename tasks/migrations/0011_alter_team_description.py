# Generated by Django 4.2.6 on 2023-12-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_remove_team_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]