from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.IntegerField(unique=True, max_length=4)
    total_earned = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Shift(models.Model):
    worker = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(null = True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_earned = models.FloatField()
    base_pay = models.FloatField(default=0)
    evening_penalties = models.FloatField(default=0)
    night_penalties = models.FloatField(default=0)
    saturday_pay = models.FloatField(default=0)
    sunday_pay = models.FloatField(default=0)
    overtime_level_1 = models.FloatField(default=0)
    overtime_level_2 = models.FloatField(default=0)
    overtime_weekend = models.FloatField(default=0)
    holiday_pay = models.FloatField(default=0)
    meal_break_taken = models.BooleanField(default=False)
    meal_break_start = models.TimeField(blank=True, null=True)
    meal_break_end = models.TimeField(blank=True, null=True)
    paid = models.BooleanField(default= False)
    
    # Somehow check that the user mfin inputted end time isn't before the start time
    # Mfers be doin dis and dat then saying the program doesn't work

    def __str__(self):
        return str(self.date)




