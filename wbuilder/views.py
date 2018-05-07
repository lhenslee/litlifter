from django.shortcuts import render
from django.core import management
from membership.models import Account
import sys, os
from . import workout
from django.core.mail import send_mail
from newworkouts.models import (Post_workout)


content = {}
content['profile'] = 'Login'
content['signup'] = 'Sign Up'
inputs = {}

def set_workout_numbers(equips):
    available_workouts = {}
    for w in Post_workout.objects.all():
        for equip in equips:
            if w.equipment == equip:
                available_workouts.setdefault(w.musclegroup, [])
                available_workouts[w.musclegroup].append(w)
    try: content['calves'] = len(available_workouts['Calves'])
    except Exception: pass
    try: content['chest'] = len(available_workouts['Chest'])
    except Exception: pass
    try: content['middleback'] = len(available_workouts['Middle Back'])
    except Exception: pass
    try: content['lowerback'] = len(available_workouts['Lower Back'])
    except Exception: pass
    try: content['lats'] = len(available_workouts['Lats'])
    except Exception: pass
    try: content['quadriceps'] = len(available_workouts['Quadriceps'])
    except Exception: pass
    try: content['hamstrings'] = len(available_workouts['Hamstrings'])
    except Exception: pass
    try: content['glutes'] = len(available_workouts['Glutes'])
    except Exception: pass
    try: content['shoulders'] = len(available_workouts['Shoulders'])
    except Exception: pass
    try: content['biceps'] = len(available_workouts['Biceps'])
    except Exception: pass
    try: content['triceps'] = len(available_workouts['Triceps'])
    except Exception: pass
    try: content['abdominals'] = len(available_workouts['Abdominals'])
    except Exception: pass 
    try: content['traps'] = len(available_workouts['Traps'])
    except Exception: pass

def index(request):
    
    if request.method == 'POST': 
        if request.POST['submission'] == 'submit': 
            workout.Exercise.exercises = []
            inputs['groups'] = request.POST.getlist('musclegroups') 
            inputs['wtype'] = request.POST['extype']
            inputs['equip'] = request.POST['equipment']
            inputs['wnumber'] = int(request.POST['wnumber'])
            inputs['difficulty'] = request.POST['difficulty']
            try:
                user = Account.objects.get(username=request.session['member'])
                inputs['difficulty'] = user.experience
                inputs['equip'] = user.equipment.split(',')
                set_workout_numbers(inputs['equip'])
                print(inputs['difficulty'] + ' for ' + user.username)
            except Exception as e: print(e)
            try:
                workout.custom_workout(inputs['equip'], inputs['wtype'], inputs['groups'], inputs['wnumber'], inputs['difficulty'])
                content['exercises'] = workout.Exercise.exercises
                return render(request, 'handmade/workout.html', content)
            except Exception as e: 
                content['exercises'] = [workout.Exercise('Not enough workouts in one or more musclegroups', '', 'Sets', 'Reps')]
                return render(request, 'handmade/workout.html', content)
        if request.POST['submission'] == 'reshuffle': 
            workout.Exercise.exercises = []
            try:
                print(inputs)
                workout.custom_workout(inputs['equip'], inputs['wtype'], inputs['groups'], inputs['wnumber'], inputs['difficulty'])
                content['exercises'] = workout.Exercise.exercises
                return render(request, 'handmade/workout.html', content)
            except Exception as e: 
                print(e)
                content['exercises'] = [workout.Exercise('Not enough workouts in one or more musclegroups', '', 'Sets', 'Reps')]
                return render(request, 'handmade/workout.html', content)
        if request.POST['submission'] == 'email': 
            email = Account.objects.get(username=request.session['member']).email
            management.call_command('send_email', email)
            return render(request, 'handmade/workout.html', content)
    try: 
        user = Account.objects.get(username=request.session['member'])
        set_workout_numbers(user.equipment.split(','))
        content['profile'] = user.username.capitalize()
    except Exception as e: print(e)
    return render(request, 'handmade/workout.html', content)

def makelift(request):
    yes = []
    if request.method == "POST":
        print(request.POST)
        groups = request.POST.getlist('musclegroups') 
        wtypes = request.POST.getlist('extype')
        equips = request.POST.getlist('equipment')
        wnumbers = request.POST.getlist('wnumber')
        difficulty = request.POST.getlist('difficulty')
        if len(wtypes) > 0: wtype = wtypes[0]
        else: wtype = 'mixed'
        if len(equips) > 0: equip = equips[0]
        else: equip = 'weighted'
        if wnumbers[0] != '': wnumber = wnumbers[0]
        else: wnumber = '2'
        if len(difficulty) > 0: difficulty = difficulty[0]
        else: difficulty = 'intermediate'
        try:
            user = Account.objects.get(username=request.session['member'])
            print(user)
            difficulty = user.experience
            equip = user.equipment.split(',')
            print(difficulty + ' for ' + user.username)
        except Exception as e: print(e)
        try:
            workout.custom_workout(equip, wtype, groups, int(wnumber), difficulty)
            #print(workout.Exercise.exercises)
            return render(request, 'handmade/workout.html', content)
        except Exception as e: return render(request, 'wbuilder/error.html', content)
    elif request.GET['Submit'] == 'Send Email to Myself':
        email = Account.objects.get(username=request.session['member']).email
        management.call_command('send_email', email)
        return render(request, 'handmade/workout.html')
    return render(request, 'handmade/workout.html', content)

