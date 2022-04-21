# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm, ForgetPass, ResetPass
from django.contrib.auth.models import User
from .models import ResetPassLink
import hashlib
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from .send_mail import sendResetMail
import pytz


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def forget_pass(request):
    form = ForgetPass(request.POST or None)

    msg = None
    status_code = None # 1 = successful, -1 = failure

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            # print("Username:", username)
            inp_user = User.objects.filter(username=username)
            # print("Inp user:", inp_user)
            if (len(inp_user) > 0):
                msg = "Reset password by the link sent via email"
                status_code = 1
                reset_link = createResetPassLink(inp_user[0])
                dist_email = inp_user[0].email
                print("Dist email:", dist_email)
                print("Reset link:", reset_link)
                sendResetMail(dist_email, reset_link)
            else:
                msg = "Wrong credentials, try again"
                status_code = -1
        else:
            msg = 'Error validating the form'
            status_code = -1

    return render(request, "accounts/forget_pass.html", {"form": form, "msg": msg, "status": status_code})

def createResetPassLink(user):
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    str = user.username + now_str
    result = hashlib.md5(str.encode()).hexdigest()
    expire = now + timedelta(hours=1)
    link_save = ResetPassLink(user=user, link=result, expire_time=expire)
    link_save.save()
    return result

def reset_pass(request, link):
    form = ResetPass(request.POST or None)

    msg = None
    status_code = 1 # 1 = newly created, 2 = successful, -1 = invalid reset code + link expired, -2 = error validating form
    
    utc = pytz.UTC
    reset_link_valid = get_object_or_404(ResetPassLink, link=link)
    if reset_link_valid is None:
        msg = "Reset code invalid"
        status_code = -1
    elif reset_link_valid.expire_time < utc.localize(datetime.now()):
        reset_link_valid.delete()
        msg = "Link expired"
        status_code = -1
    elif request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data.get("password")
            repassword = form.cleaned_data.get("re_password")
            if password != repassword:
                msg = 'Password not match'
                status_code = -2
            elif len(password) < 8:
                msg = 'Password len must be at least 8 letters'
                status_code = -2
            else:
                user_change_pass = User.objects.get(username=reset_link_valid.user)
                user_change_pass.set_password(password)
                user_change_pass.save()
                reset_link_valid.delete()
                msg = 'Reset password successfully'
                status_code = 2
        else:
            msg = 'Error validating the form'
            status_code = -2

    return render(request, "accounts/reset_pass.html", {"form": form, "msg": msg, "status": status_code})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
