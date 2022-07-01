# Generated by Django 4.0.1 on 2022-06-17 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_remove_usermodel_shifts_usermodel_shifts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='shifts',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='username',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='pin',
            field=models.IntegerField(default=4305, max_length=4, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usermodel',
            name='total_earned',
            field=models.IntegerField(default=0),
        ),
    ]
