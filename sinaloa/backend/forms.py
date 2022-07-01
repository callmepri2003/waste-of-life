
from tkinter import Label
from django import forms

class ShiftForm(forms.Form):
    pin = forms.IntegerField(label='Pin : ')
    date = forms.DateField(label='Date')
    start_time = forms.TimeField(label = 'Start time')
    end_time = forms.TimeField(label = 'End time')
    meal_break_taken = forms.BooleanField(label= 'Meal Break', required = False)
    meal_break_start_time = forms.TimeField(label = 'Taken at: ', required= False)
    meal_break_end_time = forms.TimeField(label= 'Until: ', required= False)
