from django.core.management.base import BaseCommand, CommandError
from django.views.generic import ListView, DetailView
import numpy as np
import random
from django.shortcuts import render
from newworkouts.models import (Post_workout,
                                Rep_Configurations,
                                Set_Configurations,
                                Time_Configurations)
from django.core.cache import cache


class SetTypes(object):
    set_types = []
    
    def __init__(self, easy_sets, intermediate_sets, hard_sets, extreme_sets):
        self.easy = easy_sets
        self.intermediate = intermediate_sets
        self.hard = hard_sets
        self.extreme = extreme_sets

    def __str__(self):
        return 'Easy ' + self.easy_sets


class RepTypes(object):
    rep_types = []
    
    def __init__(self, purpose, easy_reps, intermediate_reps, hard_reps, extreme_reps):
        self.purpose = purpose
        self.easy = easy_reps
        self.intermediate = intermediate_reps
        self.hard = hard_reps
        self.extreme = extreme_reps


class Workout(object):
    workouts = []
    workout_dic = {}
    difficulty = ''
    email = ''

    def __init__(self, title='', rating='',
                 link='', muscle='', equip='', purpose=''):
        self.title = title
        self.rating = rating
        self.videolink = link
        self.musclegroup = muscle
        self.equipment = equip
        self.purpose = purpose
            

    def __repr__(self):
        return self.title

    def __str__(self):
        return '{},{},{},{},{},{}\n'.format(self.title,
                                         self.rating,
                                         self.videolink,
                                         self.musclegroup,
                                         self.equipment,
                                            self.reps)


def charfield_to_list(var):
    ''.join(var)
    reps = var.split(',')
    return reps

def set_types():
    sets = Set_Configurations.objects.get(id=1)
    easy_sets = charfield_to_list(sets.easy_sets)
    intermediate_sets = charfield_to_list(sets.intermediate_sets)
    hard_sets = charfield_to_list(sets.hard_sets)
    extreme_sets = charfield_to_list(sets.extreme_sets)
    SetTypes.set_types = SetTypes(easy_sets, intermediate_sets, hard_sets, extreme_sets)

def rep_types():
    for item in Rep_Configurations.objects.all():
        easy_reps = charfield_to_list(item.easy_reps)
        intermediate_reps = charfield_to_list(item.intermediate_reps)
        hard_reps = charfield_to_list(item.hard_reps)
        extreme_reps = charfield_to_list(item.extreme_reps)
        rep_type = RepTypes(item.purpose, easy_reps, intermediate_reps, hard_reps, extreme_reps)
        RepTypes.rep_types.append(rep_type)
    
def obj_from_list(thelist, index, value):
    for obj in thelist:
        obj_dict = obj.__dict__
        if obj_dict[index] == value:
            dic = obj.__dict__
            return obj

def set_html_row(line):
    return '<tr><td>' + '</td><td>'.join(line) + '</td></tr>'
	
def str_to_list(var):
    return var.replace('[','').replace(']','').replace(' ','').replace('\'','').split(',')

def set_html_link(link, title):
    return '<a class=\"video-link\" target=\"blank\" href=\"' + link + '\">' + title + '</a>'

def build_musclegroup_dict():
    for workout in Workout.workouts:
        Workout.workout_dic.setdefault(workout.musclegroup, [])
        Workout.workout_dic[workout.musclegroup].append(workout)

def get_weights():
    for item in Post_workout.objects.all():
        if (item.equipment != 'Other' and item.equipment != 'Body Only' and
            item.equipment != 'Kettlebells' and item.equipment != 'None'
            and item.rating > 8.5):
            workout = Workout(item.title, item.rating, item.videolink, item.musclegroup.replace(' ', ''), item.equipment, item.purpose)
            Workout.workouts.append(workout)
    build_musclegroup_dict()
    Workout.reps = [6, 8, 10, 12]

def get_bodyweights():
    for item in Post_workout.objects.all():
        if item.equipment == 'None' or item.equipment == 'Body Only':
            workout = Workout(item.title, item.rating, item.videolink, item.musclegroup.replace(' ', ''), item.equipment, item.purpose)
            Workout.workouts.append(workout)
    build_musclegroup_dict()
    Workout.reps = [6, 8, 10, 12]

def get_mixedweights():
    for item in Post_workout.objects.all():
        if item.equipment != 'Kettlebells':
            workout = Workout(item.title, item.rating, item.videolink, item.musclegroup.replace(' ', ''), item.equipment, item.purpose)
            Workout.workouts.append(workout)
    build_musclegroup_dict()
    Workout.reps = [6, 8, 10, 12, 15]

def make_rand_exercise(musclegroup):
    workout = random.choice(Workout.workout_dic[musclegroup])
    ex = set_html_link(workout.videolink, workout.title)
    set_dict = SetTypes.set_types.__dict__
    setnum = str(random.choice(set_dict[Workout.difficulty]))
    reptype = workout.purpose
    rep_dict = obj_from_list(RepTypes.rep_types, 'purpose', reptype).__dict__
    repnum = random.choice(rep_dict[Workout.difficulty])
    if len(repnum.split('-')) > 1: setnum = str(len(repnum.split('-')))
    exlink = workout.videolink
    line = ex, setnum, repnum
    Workout.workouts.remove(workout)
    Workout.workout_dic[musclegroup].remove(workout)
    return set_html_row(line)

def make_rand_superset(musclegroup):
    workout = random.choice(Workout.workout_dic[musclegroup])
    ex = set_html_link(workout.videolink, workout.title)
    set_dict = SetTypes.set_types.__dict__
    setnum = str(random.choice(set_dict[Workout.difficulty]))
    reptype = workout.purpose
    rep_dict = obj_from_list(RepTypes.rep_types, 'purpose', reptype).__dict__
    repnum = random.choice(rep_dict[Workout.difficulty])
    if len(repnum.split('-')) > 1: repnum = random.choice(rep_dict[Workout.difficulty])
    exlink = workout.videolink
    line = ex, 'Superset', repnum
    Workout.workouts.remove(workout)
    Workout.workout_dic[musclegroup].remove(workout)
    return set_html_row(line)

def make_rand_burnout(musclegroup):
    workout = random.choice(Workout.workout_dic[musclegroup])
    ex = set_html_link(workout.videolink, workout.title)
    set_dict = SetTypes.set_types.__dict__
    setnum = str(random.choice(set_dict[Workout.difficulty]))
    reptype = workout.purpose
    rep_dict = obj_from_list(RepTypes.rep_types, 'purpose', reptype).__dict__
    repnum = random.choice(rep_dict[Workout.difficulty])
    if len(repnum.split('-')) > 1: setnum = str(len(repnum.split('-')))
    link = workout.videolink
    line = ex, 'Burnout: ' + setnum, repnum
    Workout.workouts.remove(workout)
    Workout.workout_dic[musclegroup].remove(workout)
    return set_html_row(line)
    
def file_setup(filename):
    f = open(filename, 'w')
    f.write('{% extends "personal/header.html" %}{% block content %}'+
            '{% include "wbuilder/includes/checkboxes.html" %}<table class=\"col-sm-8\">') 
    headers = 'Exercise', 'Sets', 'Reps'
    f.write('<tr><th>' + '</th><th>'.join(headers) + '</th></tr>')
    f.close()

def mixed_routine(filename, groups, pergroup):
    liftgroup = []
    ltypes = [make_rand_exercise, make_rand_exercise, make_rand_exercise, make_rand_exercise, 
              make_rand_exercise, make_rand_superset, make_rand_superset, make_rand_superset,
              make_rand_burnout]
    for i in range(pergroup):
        random.shuffle(groups)
        for group in groups:
            liftgroup.append(group)
    f = open(filename, 'a')
    f.write(make_rand_exercise(liftgroup[0]))
    liftgroup.remove(liftgroup[0])
    for lift in liftgroup:
        f.write(random.choice(ltypes)(lift))
    f.close()

def solos_routine(filename, groups, pergroup):
    liftgroup = []
    for i in range(pergroup):
        random.shuffle(groups)
        for group in groups:
            liftgroup.append(group)
    f = open(filename, 'a')
    for lift in liftgroup:
        f.write(make_rand_exercise(lift))
    f.close()

def superset_routine(filename, groups, pergroup):
    liftgroup = []
    for i in range(pergroup):
        random.shuffle(groups)
        for group in groups:
            liftgroup.append(group)
    f = open(filename, 'a')
    for i in range(int(len(liftgroup)/2)):
        f.write(make_rand_exercise(liftgroup[2*i]))
        try:
            f.write(make_rand_superset(liftgroup[2*i+1]))
        except Exception as e:
            print(e)
    f.close()

def burnout_routine(filename, groups, pergroup):
    liftgroup = []
    for i in range(pergroup):
        random.shuffle(groups)
        for group in groups:
            liftgroup.append(group)
    f = open(filename, 'a')
    for lift in liftgroup:
        f.write(make_rand_burnout(lift))
    f.close()

def cycle_routine(filename, groups, pergroup):
    liftgroup = []
    for i in range(pergroup):
        for group in groups:
            liftgroup.append(group)
    random.shuffle(liftgroup)
    f = open(filename, 'a')
    f.write(make_rand_exercise(liftgroup[0]))
    liftgroup.remove(liftgroup[0])
    for lift in liftgroup:
        f.write(make_rand_superset(lift))
    f.close()

def favorite_routine(filename, groups):
    f = open(filename, 'a')
    for group in groups:
        for i in range(2):
            f.write(make_rand_exercise(group))
    for i in range(2):
        f.write(make_rand_exercise(groups[0]))
        for group in groups[1:]:
            f.write(make_rand_superset(group))
    for group in groups:
        f.write(make_rand_burnout(group))
    f.close()

def custom_workout(equip, wtype, groups, pergroup):
    filename = 'C:/Users/Lane/Documents/Lift my Python/mysite/wbuilder/templates/wbuilder/workout.html'
    file_setup(filename)
    rep_types()
    set_types()
    if equip == 'weighted':
        get_weights()
    elif equip == 'bodyweight':
        get_bodyweights()
    else:
        get_mixedweights()
    if wtype == 'soloex':
        solos_routine(filename, groups, pergroup)
    elif wtype == 'superset':
        superset_routine(filename, groups, pergroup)
    elif wtype == 'burnout':
        burnout_routine(filename, groups, pergroup)
    elif wtype == 'cycle':
        cycle_routine(filename, groups, pergroup)
    elif wtype == 'favorite':
        favorite_routine(filename, groups)
    else:
        mixed_routine(filename, groups, pergroup)
    f = open(filename, 'a')
    f.write('<form><tr><td><input type="submit" value="Send Email to Myself" name="Submit" style="color:black"><td></tr></form>')
    f.write('</table> {% endblock %}')
    Workout.workout_dic = {}
    Workout.workouts = []
    groups = []
    
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('yes')
        parser.add_argument('group_string')
    def handle(self, *args, **options):
        groups = []
        groups = str_to_list(options['yes'])
        wtype = groups[0]
        groups.remove(wtype)
        equip = groups[0]
        groups.remove(equip)
        pergroup = groups[0]
        groups.remove(pergroup)
        Workout.difficulty = str(groups[0])
        groups.remove(Workout.difficulty)
        custom_workout(equip, wtype, groups, int(pergroup))
