from contextlib import redirect_stderr
from email.mime import base
from tracemalloc import start
from django.shortcuts import render, redirect

from datetime import *

from .forms import ShiftForm
from .models import Shift, UserModel

from django.contrib.auth.models import User

# Create your views here.
def calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT):
                base_pay = 0
                evening_pay = 0
                night_pay = 0
                base_pay = hours_worked * pay_rates['base']


                # Calculating evening pay

                if datetime.strptime(start_time, FMT) < datetime.strptime('19:00:00', FMT) and datetime.strptime(end_time, FMT) < datetime.strptime('07:00:00', FMT):
                    
                    evening_pay = 5 * pay_rates['weekday_evening']
                elif datetime.strptime(start_time, FMT) > datetime.strptime('19:00:00', FMT) and datetime.strptime(end_time, FMT) < datetime.strptime('23:59:00', FMT):
                    
                    evening_pay = hours_worked * pay_rates['weekday_evening']
                elif datetime.strptime(start_time, FMT) < datetime.strptime('19:00:00', FMT) and datetime.strptime(end_time, FMT) < datetime.strptime('23:59:00', FMT) and datetime.strptime(end_time, FMT) > datetime.strptime('19:00:00', FMT):
                    
                    evening_hours = datetime.strptime(end_time, FMT) - datetime.strptime('19:00:00', FMT)
                    evening_hours = float(evening_hours.total_seconds()/3600)
                    evening_pay = evening_hours * pay_rates['weekday_evening']
                elif datetime.strptime(start_time, FMT) > datetime.strptime('19:00:00', FMT) and datetime.strptime(end_time, FMT) < datetime.strptime('07:00:00', FMT) and datetime.strptime(start_time, FMT) < datetime.strptime('23:59:00', FMT):
                    
                    evening_hours = datetime.strptime('11:59:00', FMT) - datetime.strptime(start_time, FMT)
                    evening_hours = float(evening_hours.total_seconds()/3600)
                    evening_pay = evening_hours * pay_rates['weekday_evening']
                    
                # Calculating night pay

                if datetime.strptime(end_time, FMT) > datetime.strptime('00:00:00', FMT) and datetime.strptime(end_time, FMT) < datetime.strptime('07:00:00', FMT):
                    night_hours = datetime.strptime(end_time, FMT) - datetime.strptime('00:00:00', FMT)
                    night_hours = float(night_hours.total_seconds()/3600)
                    night_pay = night_hours * pay_rates['weekday_night']
                
                print(evening_pay)
                return [base_pay + evening_pay + night_pay, evening_pay, night_pay, base_pay]

def calculate_pay(data):
    # Calculate pay
            
            pay_rates = {
                'base': 26.15,
                'weekday_evening': 2.37,
                'weekday_night': 3.55,
                'saturday': 31.38,
                'sunday': 36.61,
                'weekday_overtime_first_2': 31.38,
                'weekday_overtime_ultimate': 41.84,
                'weekend_overtime': 41.84,
                'holiday': 52.30
            }
            max_weekday_overtime1_pay = 2 * pay_rates['weekday_overtime_first_2']

            # Calculate amount of hours worked
            FMT = '%H:%M:%S'
            start_time = str(data['start_time'])
            end_time = str(data['end_time'])
            hours_worked = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
            
            # Make sure hours after midnight are calculated as AFTER not BEFORE
            if hours_worked.days < 0:
                hours_worked = timedelta(
                    days=0,
                    seconds=hours_worked.seconds,
                    microseconds=hours_worked.microseconds
                )
            
            hours_worked = float(hours_worked.total_seconds()/3600)

            holiday = False
            weekend = [0,0]

            if(data['date'].weekday() == 5):
                weekend[0] = 1
            elif(data['date'].weekday() == 6):
                weekend[1] = 1

            total_pay = 0
            base_pay = 0
            evening_pay = 0
            night_pay = 0
            saturday_pay = 0
            sunday_pay = 0
            overtime_level_1 = 0
            overtime_level_2 = 0
            overtime_weekend = 0
            holiday_pay = 0


            if holiday:
                holiday_pay = hours_worked * pay_rates['holiday']
                
            elif weekend[0] or weekend[1]:
                if hours_worked <= 12:
                    if weekend[0]:
                        total_pay = hours_worked * pay_rates['saturday']
                        saturday_pay = total_pay
                    elif weekend[1]:
                        total_pay = hours_worked * pay_rates['sunday']
                        sunday_pay = total_pay
                else:
                    if weekend[0]:
                        overtime_weekend = (hours_worked - 12) * pay_rates['weekend_overtime']
                        saturday_pay = 12 * pay_rates['saturday']
                        total_pay = saturday_pay + overtime_weekend

                    elif weekend[1]:
                        overtime_weekend = (hours_worked - 12) * pay_rates['weekend_overtime']
                        sunday_pay = 12 * pay_rates['sunday']
                        total_pay = sunday_pay + overtime_weekend
            else:
                if hours_worked <= 12:
                    weekday_non_overtime_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[0]
                    total_pay = weekday_non_overtime_pay
                    evening_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[1]
                    night_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[2]
                    base_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[3]


                elif hours_worked <= 14:
                    
                    # Add 12 hours
                    holder = int(start_time[0:2]) + 12
                    if holder >= 24:
                        holder -= 24
                    non_overtime_end_time = str(holder) + start_time[2:]
                    
                    weekday_non_overtime_pay = calculate_non_overtime_pay(start_time, non_overtime_end_time, pay_rates, 12, FMT)[0]
                    evening_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[1]
                    night_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[2]
                    base_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[3]

                    weekday_overtime1_hours = hours_worked - 12
                    weekday_overtime1_pay = weekday_overtime1_hours * pay_rates['weekday_overtime_first_2']
                    
                    total_pay = weekday_non_overtime_pay + weekday_overtime1_pay
                    
                    
                else:
                    # Add 12 hours
                    holder = int(start_time[0:2]) + 12
                    if holder >= 24:
                        holder -= 24
                    non_overtime_end_time = str(holder) + start_time[2:]
                    weekday_non_overtime_pay = calculate_non_overtime_pay(start_time, non_overtime_end_time, pay_rates, 12, FMT)[0]
                    evening_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[1]
                    night_pay = calculate_non_overtime_pay(start_time, end_time, pay_rates, hours_worked, FMT)[2]
                    weekday_overtime2_hours = hours_worked - 14
                    weekday_overtime2_pay = weekday_overtime2_hours * pay_rates['weekday_overtime_ultimate']
                    total_pay = weekday_overtime2_pay + weekday_non_overtime_pay + max_weekday_overtime1_pay

                    base_pay = weekday_non_overtime_pay
                    overtime_level_1 = max_weekday_overtime1_pay
                    overtime_level_2 = weekday_overtime2_pay

            return [total_pay, base_pay, evening_pay, night_pay, saturday_pay, sunday_pay, overtime_level_1, overtime_level_2, overtime_weekend, holiday_pay]

def home_view(request):

    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            # Get user
            
            pay_data = calculate_pay(form.cleaned_data)
            


            
            

            total_pay = pay_data[0]
            base_pay = pay_data[1]
            evening_pay = pay_data[2]
            night_pay = pay_data[3]
            saturday_pay = pay_data[4]
            sunday_pay = pay_data[5]
            overtime_level_1 = pay_data[6]
            overtime_level_2 = pay_data[7]
            overtime_weekend = pay_data[8]
            holiday_pay = pay_data[9]
            meal_break_taken = form.cleaned_data['meal_break_taken']

            if(meal_break_taken):
                meal_break_data = calculate_pay({
                    'pin': form.cleaned_data['pin'],
                    'date': form.cleaned_data["date"],
                    'start_time': form.cleaned_data['meal_break_start_time'],
                    'end_time': form.cleaned_data['meal_break_end_time']
                })


                total_pay -= meal_break_data[0]
                base_pay -= meal_break_data[1]
                evening_pay -= meal_break_data[2]
                night_pay -= meal_break_data[3]
                saturday_pay -= meal_break_data[4]
                sunday_pay -= meal_break_data[5]
                overtime_level_1 -= meal_break_data[6]
                overtime_level_2 -= meal_break_data[7]
                overtime_weekend -= meal_break_data[8]
                holiday_pay -= meal_break_data[9]
            
            

            
            worker = UserModel.objects.get(pin = form.cleaned_data['pin'])
            
            





            Shift(meal_break_taken = meal_break_taken, worker = worker, date = form.cleaned_data['date'], start_time = form.cleaned_data['start_time'], end_time = form.cleaned_data['end_time'], total_earned = total_pay, base_pay = base_pay, evening_penalties = evening_pay, night_penalties = night_pay, saturday_pay = saturday_pay, sunday_pay = sunday_pay, overtime_level_1 = overtime_level_1, overtime_level_2 = overtime_level_2, overtime_weekend = overtime_weekend, holiday_pay = holiday_pay, meal_break_start = form.cleaned_data['meal_break_start_time'], meal_break_end = form.cleaned_data['meal_break_end_time']).save()
            return redirect('/')
    elif request.method == 'GET':
        try:

            if 'date' in request.GET:
                print('testing')
                obj = Shift.objects.get(date = datetime.strptime(request.GET['date'], "%Y-%m-%d" ))
                
                obj.paid = True
                obj.save()
                # print(Shift.objects.get(date = request.GET['date']).paid)
                

            targetUser = UserModel.objects.get(pin = request.GET['pin'])
            
            targetShifts = Shift.objects.filter(worker = targetUser)
            totalOwed = 0
            for shift in list(targetShifts):
                if shift.paid == False:
                    totalOwed += shift.total_earned
            
            form = ShiftForm()



            context = {
                'form': form,
                'shifts': list(targetShifts),
                'total_owed': totalOwed,
                'display' : True,
                'pin': request.GET['pin']
            }
        except:
            form = ShiftForm()

            context = {
                'form': form,
                'display' : False
            }

    return render(request, 'home.html', context)