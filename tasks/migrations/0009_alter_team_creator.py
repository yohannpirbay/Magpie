# Generated by Django 4.2.6 on 2023-12-01 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_team_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_teams', to=settings.AUTH_USER_MODEL),
        ),
    ]
