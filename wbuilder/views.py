from django.shortcuts import render
from django.core import management
from membership.models import Account
import sys, os
from . import workout
from django.core.mail import send_mail
from newworkouts.models import (Post_workout)

def initContent():
    content = {}
    content['profile'] = 'Login'
    content['signup'] = 'Sign Up'
    content['equips'] = []
    return content

def makeWorkout(inputs):
    if inputs['groups']:
        workout.custom_workout(inputs['equips'], inputs['wtype'], 
        inputs['groups'], inputs['wnumber'], inputs['difficulty'])
        return workout.Exercise.exercises

def index(request):

    # Initialize content
    content = initContent()
    availableWorkouts = {}
    workoutInputs = {}
    workoutInputs['equips'] = []
    workoutInputs['wtype'] = ''
    workoutInputs['groups'] = []
    workoutInputs['wnumber'] = 0
    workoutInputs['difficulty'] = ''

    # Get the current user data
    try:
        user = Account.objects.get(username=request.session['member'])
        content['profile'] = user.username.capitalize()
        content['signup'] = 'Logged in'
        workoutInputs['equips'] = user.equipment.split(',')
        for w in Post_workout.objects.all():
            for equip in workoutInputs['equips']:
                if w.equipment == equip:
                    availableWorkouts.setdefault(w.musclegroup, [])
                    availableWorkouts[w.musclegroup].append(w)
                    content[w.musclegroup.replace(' ', '')] = (
                        '(' + str(len(availableWorkouts[w.musclegroup])) + ')')
        workoutInputs['difficulty'] = user.experience
    except Exception: pass

    # Handle post requests
    if request.method == 'POST': 
        # The first workout submission
        if request.POST['submission'] == 'submit':
            content['exercises'] = []
            workout.Exercise.exercises = []
            # Get workout inputs
            if not workoutInputs['equips'] and not workoutInputs['difficulty']:
                workoutInputs['equips'] = ['Barbell', 'Dumbbell', 'Machine', 'None']
                workoutInputs['difficulty'] = 'intermediate'
            if len(request.POST.getlist('equipment')) > 0:
                workoutInputs['equips'] = request.POST.getlist('equipment')
            workoutInputs['groups'] = request.POST.getlist('musclegroups') 
            workoutInputs['wtype'] = 'mixed'
            workoutInputs['wnumber'] = 2
            if request.POST['wnumber']:
                workoutInputs['wnumber'] = int(request.POST['wnumber'])
            # Build a workout if a group is selected
            if workoutInputs:
                content['exercises'] = makeWorkout(workoutInputs)

        # Reshuffle the workout with the same inputs
        if request.POST['submission'] == 'reshuffle':
            print('reshuffle')

    # Render the workout html
    return render(request, 'handmade/workout.html', content)