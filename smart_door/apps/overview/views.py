# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import imp
from multiprocessing import context
from re import S
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import Room, Schedule, Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

now = datetime.now()


@login_required(login_url="/login/")
def admin_overview(request):
    profile = request.user
    super_user = User.objects.filter(is_superuser=True)
    if not (profile in super_user): return HttpResponse("<h1>Not allowed</h1>");
    context = {}
    html_template = loader.get_template('overview/overview.html')
    return HttpResponse(html_template.render(context, request))
    # context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    # try:

    #     load_template = request.path.split('/')[-1]

    #     if load_template == 'admin':
    #         return HttpResponseRedirect(reverse('admin:index'))
    #     context['segment'] = load_template

    #     html_template = loader.get_template('home/' + load_template)
    #     return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))
    
    

@csrf_exempt
def add_sched(request):
    profile = request.user.profile
    if request.is_ajax() and request.method == "POST":
        time = int(request.POST.get("time", ""))
        date_time = request.POST.get("datetime", "")
        date_time = datetime.strptime(date_time, '%d/%m/%Y').date()
        room = request.POST.get("room", "")
        room = get_object_or_404(Room, slug=room)
        new_obj = Schedule(room=room, user=profile.user, time_slot=time, schedule_date=date_time)
        new_obj.save()
        return JsonResponse({"succ":"successful"}, status=200)
    return JsonResponse({"error":"not valid"}, status=400)
