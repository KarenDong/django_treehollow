# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.db import models
from models import User, Hollow
from django.contrib import messages
import datetime
import re
import bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        pw_conf = request.POST['pw_conf']
        dob = request.POST['dob']
        print "checking information..."
        error1 = User.objects.register(name,alias,email,password,pw_conf,dob)
        if error1:
            for error in error1:
                messages.error(request, error)
            return redirect('/')
        else:
            print "User is being created..."
            messages.success(request, 'You Just registered an account!')
            return redirect('/')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print "checking information..."
        error2 = User.objects.login(email,password)
        if error2:
            for error in error2:
                messages.error(request, error)
            return redirect('/')
        else:
            print "Login to the account..."
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            return redirect('/hollow')

def hollow(request):
    me = User.objects.get(id=request.session['id'])
    all_hollow = Hollow.objects.filter(writer = me)
    try:
        my_hollow = []
        my_hollow = all_hollow
    except:
        all_hollow = None
    context = {
        "me":me,
        "hollows":my_hollow
    }
    return render(request, "first_app/home.html", context)

def add(request):
    if request.method == "POST":
        a_topic = request.POST['topic']
        a_content = request.POST['content']
        print "checking input..."
        error1 = Hollow.objects.add(request.session["id"], a_topic, a_content)
        if error1:
            for error in error1:
                messages.error(request, error)
            return redirect('/hollow')
        else:
            print "Hollow of is being created..."
            return redirect('/hollow')

def viewUser(request, id):
    friend_info = User.objects.get(id=id)
    context ={
        "user": friend_info
    }
    return render(request, "first_app/user.html", context)

def viewHollow(request, id):
    thishollow = Hollow.objects.get(id=id)
    context ={
        "hollow": thishollow
    }
    return render(request, "first_app/hollow.html", context)

def remove(request, id):
    Hollow.objects.remove(id)
    return redirect('/hollow')

def logout(request):
    request.session['id'] = 0
    return redirect('/')
