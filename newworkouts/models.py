from django.db import models
import numpy as np


class Post_workout(models.Model):
    title = models.CharField(max_length=140)
    rating = models.FloatField()
    videolink = models.CharField(max_length=140)
    musclegroup = models.CharField(max_length=140)
    equipment = models.CharField(max_length=140)
    purpose = models.CharField(max_length=140)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Set_Configurations(models.Model):
    easy_sets = models.CharField(max_length=140)
    intermediate_sets = models.CharField(max_length=140)
    hard_sets = models.CharField(max_length=140)
    extreme_sets = models.CharField(max_length=140)


class Time_Configurations(models.Model):
    easy_timer = models.CharField(max_length=140)
    intermediate_timer = models.CharField(max_length=140)
    hard_timer = models.CharField(max_length=140)
    extreme_timer = models.CharField(max_length=140)


class Rep_Configurations(models.Model):
    purpose = models.CharField(max_length=140)
    easy_reps = models.CharField(max_length=140)
    intermediate_reps = models.CharField(max_length=140)
    hard_reps = models.CharField(max_length=140)
    extreme_reps = models.CharField(max_length=140)

    def __str__(self):
        return self.purpose


def edit_reps():
##    for item in Post_workout.objects.filter(equipment='Barbell'):
##        item.reps = 'reps_1'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Dumbbell'):
##        item.reps = 'reps_2'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Exercise Ball'):
##        item.reps = 'reps_3'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Cable'):
##        item.reps = 'reps_4'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='E-Z Curl Bar'):
##        item.reps = 'reps_5'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Machine'):
##        item.reps = 'reps_6'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Medicine Ball'):
##        item.reps = 'reps_7'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='None'):
##        item.reps = 'reps_8'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Other'):
##        item.reps = 'reps_9'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Body Only'):
##        item.reps = 'reps_10'
##        item.save()
##    for item in Post_workout.objects.filter(equipment='Bands'):
##        item.reps = 'reps_12'
##        item.save()
    for item in Post_workout.objects.all():
        item.purpose = item.equipment
        item.save()

def set_database_from_csv():  
    titles = np.loadtxt('workouts.csv',
                        delimiter=',',
                        dtype='str',
                        skiprows=1)
    for i in range(len(titles)):
        Post_workout.objects.create(title=titles[i][0],rating=titles[i][1],videolink=titles[i][2],
                                    musclegroup=titles[i][3],equipment=titles[i][4],reps=reps)
