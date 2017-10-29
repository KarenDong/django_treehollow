# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
import datetime
NAME_REGEX = re.compile(r'^[A-Za-z ]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')

class userManager(models.Manager):
    def register(self,name,alias,email,password,pw_conf,dob):
        error_msg = []
        if not NAME_REGEX.match(name):
            error_msg.append("Name is not valid!")

        if not EMAIL_REGEX.match(email):
            error_msg.append("Email is not valid!")
        else:
            try:
                dupli = self.get(email_iexact=email)
            except:
                dupli = None
            if dupli:
                error_msg.append("Email is registered already!")

        if len(password) < 8:
            error_msg.append("Password should have at least 8 characters!")

        if password != pw_conf:
            error_msg.append("Password do not match the confirmation!")

        if dob == None:
            error_msg.append("Birthday cannot be empty!")

        if error_msg:
            return error_msg
        else:
            pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            self.create(name=name, alias=alias, email=email, password=pw_hash, dob=dob)

    def login(self,email,password):
        msg1 = []
        try:
            user = self.get(email=email)
        except:
            user = None
        if not user:
            msg1.append("This email does not exist!")
        elif user.password != bcrypt.hashpw(password.encode(), user.password.encode()):
                msg1.append("Incorect password!")
        return msg1

    def add(self, id, a_topic, a_content):
        error_msg = []
        if a_topic == None:
            error_msg.append("The topic cannot be empty!")
        if a_content == None:
            error_msg.append("The content cannot be empty!")
        if error_msg:
            return error_msg
        else:
            self.create(writer=User.objects.get(id=id),topic=a_topic,content=a_content)

    def remove(self, hollow_id):
        thishollow = Hollow.objects.get(id = hollow_id)
        thishollow.delete()

class User(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class Hollow(models.Model):
    writer = models.ForeignKey(User, related_name="hollowwriter")
    topic = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
