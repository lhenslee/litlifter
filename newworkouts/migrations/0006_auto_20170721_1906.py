# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-22 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newworkouts', '0005_auto_20170721_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set_Configurations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('easy_sets', models.CharField(max_length=140)),
                ('intermediate_sets', models.CharField(max_length=140)),
                ('hard_sets', models.CharField(max_length=140)),
                ('extreme_sets', models.CharField(max_length=140)),
            ],
        ),
        migrations.RemoveField(
            model_name='rep_configurations',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='rep_configurations',
            name='easy_sets',
        ),
        migrations.RemoveField(
            model_name='rep_configurations',
            name='extreme_sets',
        ),
        migrations.RemoveField(
            model_name='rep_configurations',
            name='hard_sets',
        ),
        migrations.RemoveField(
            model_name='rep_configurations',
            name='intermediate_sets',
        ),
    ]
