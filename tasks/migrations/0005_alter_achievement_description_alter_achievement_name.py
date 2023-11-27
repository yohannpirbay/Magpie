# Generated by Django 4.2.6 on 2023-11-27 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_user_achievements'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='achievement',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
