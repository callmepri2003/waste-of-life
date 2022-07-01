# Generated by Django 4.0.1 on 2022-06-17 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_rename_sunday_pay_shift_sunday_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='base_pay',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='evening_penalties',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='holiday_pay',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='night_penalties',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='overtime_level_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='overtime_level_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='overtime_weekend',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='saturday_pay',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='sunday_pay',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shift',
            name='total_pay',
            field=models.IntegerField(default=0),
        ),
    ]