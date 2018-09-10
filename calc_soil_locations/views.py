from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from django.core import serializers
from .models import SoilDisposalTask

from modules.distance import sum_distance, hubeny
from modules.trajectory import get_map_html, get_trajectory_map
from modules.screenshot import shot_jpg 

import numpy as np
from numpy.random import *
import redis
import os
import time
from datetime import datetime

import subprocess

def soil_disposal_tasks_list(request):
    task_id = request.GET.get("task_id")
    _redis = redis_c()

    actual_points = fetch_locations(_redis, task_id)
    if actual_points.size == 0:
        return render(request, 'polyline/soil_disposal_tasks_list.html', {})

    print(actual_points)

    actual_points_no_time = actual_points[:,1:3]
    distance_v = sum_distance(actual_points_no_time)
    fuel_efficient = 2.5
    co2_emissions = 2.619 / fuel_efficient * distance_v
 
    task = fetch_task(task_id)
    
    distances_to_goal = hubeny(actual_points_no_time[:,0], actual_points_no_time[:,1],
            float(task.at_time_soil_disposal_site_latitude), float(task.at_time_soil_disposal_site_longitude))
    
    html = get_map_html(get_trajectory_map(
        actual_points_no_time,
        np.array([task.at_time_field_latitude, task.at_time_field_longitude]).astype(float),
        np.array([task.at_time_soil_disposal_site_latitude, task.at_time_soil_disposal_site_longitude]).astype(float)))


    task.mileage = distance_v
    task.co2_emissions = co2_emissions
    task.driving_time_second = driving_time_second(actual_points[:,0].astype(int))
    task.arrived_to_site_flg = np.any(distances_to_goal < 1000) # unit: meter
    task.image_path = settings.SOIL_LOCATIONS['default']['image_dir'] + task_id
    task.updated_at = timezone.now()
    task.save()

    return render(request, 'polyline/soil_disposal_tasks_list.html', {'soil_disposal_tasks': task, 'sum_distance': distance_v, 'html': html})

def redis_c():
    REDIS = settings.REDIS['default']
    return redis.Redis(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], encoding='utf-8', decode_responses=True)
   
def fetch_locations(_redis, task_id):
    locations = _redis.sort('soil_locations_sort_key:' + task_id, by='nosort', get='soil_locations:' + task_id + ':*')        

    actual_points = np.empty((0,3))
    for location in locations:
        actual_points = np.append(actual_points, np.array([str(location).split(':')]), axis=0)
   
    return actual_points.astype(float)  

def fetch_task(task_id):
    task = SoilDisposalTask.objects.filter(id=task_id).first()

    if task.at_time_field_latitude is None:
        raise UnboundLocalError
    if task.at_time_field_longitude is None:
        raise UnboundLocalError
    if task.at_time_soil_disposal_site_latitude is None:
        raise UnboundLocalError
    if task.at_time_soil_disposal_site_longitude is None:
        raise UnboundLocalError
    return task

def driving_time_second(times):
    time_s = time.mktime(time.strptime(str(np.amin(times)),'%Y%m%d%H%M%S'))
    time_e = time.mktime(time.strptime(str(np.amax(times)),'%Y%m%d%H%M%S'))
    return int(time_e - time_s)

def screen_shot_soil_locations_map(request):
    task_id = request.GET.get("task_id")
    subprocess.call('python manage.py shot ' + task_id + ' &', shell=True)
    json = serializers.serialize('json', SoilDisposalTask.objects.filter(id=task_id), ensure_ascii=False)
    return HttpResponse(json, content_type='application/json') 


