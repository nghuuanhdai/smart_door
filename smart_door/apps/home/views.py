# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import imp
from multiprocessing import context
import os
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Room, Schedule, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pathlib import Path
from .ml_module.people_counter import get_people_in_room_from_image

now = datetime.now()

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def rooms(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    html_template = loader.get_template('home/rooms.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def room_detail(request, room):
    room = get_object_or_404(Room, slug=room)
    context = {'room': room}
    html_template = loader.get_template('home/room_detail.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def check_schedule(request):
    card_id = request.POST.get("card_id", "")
    crr_date = datetime.now().date
    crr_time_slot = datetime.now().hour
    try:
        profile = Profile.objects.get(card_id=card_id)
        valid_schedule = Schedule.objects.filter(user=profile.user).filter(time_slot=crr_time_slot).filter(schedule_date=crr_date)
        return JsonResponse({'accessGranted': True})
    except Profile.DoesNotExist:
        return JsonResponse({'accessGranted': False})
    except Schedule.DoesNotExist:
        return JsonResponse({'accessGranted': False})

BASE_DIR = Path(__file__).resolve().parent.parent

@csrf_exempt 
def room_image_upload(request):
    room_id = request.POST.get("room_id", 0)
    image_path = handle_uploaded_room_image(room_id, request.FILES['file'])
    people_in_image = get_people_in_room_from_image(image_path)
    people_in_schedule = get_people_in_room_from_schedule(room_id)
    if people_in_image > people_in_schedule and people_in_schedule >= 0:
        send_over_crowded_warning(room_id, people_in_image, people_in_schedule)
    try:
        room = Room.objects.get(id=room_id)
        room.current_people_count = people_in_image
        room.save()
    except Room.DoesNotExist:
        print('room does not exist')
    return JsonResponse({
        'people_in_image': people_in_image,
        'people_in_schedule': people_in_schedule,
        'time': datetime.now(),
        'room_id': room_id
    })

def handle_uploaded_room_image(room_id, f):
    path = os.path.join(BASE_DIR, "static/upload/", str(room_id)+'.png')

    with open(path, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk) 
    
    return path

def get_people_in_room_from_schedule(room_id):
    try:
        room = Room.objects.get(id=room_id)
        crr_date = datetime.today()
        crr_hour = datetime.now().hour
        schedule_count = Schedule.objects.filter(room=room).filter(schedule_date=crr_date).filter(time_slot=crr_hour).count ()
        return schedule_count
    except Room.DoesNotExist:
        return -1


def send_over_crowded_warning(room_id, people_in_image, people_in_schedule):
    print(f'sending warning message {room_id}: {people_in_image}/{people_in_schedule}')
