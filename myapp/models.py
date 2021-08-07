
from django.db import models
from django.db.models.fields import CharField, EmailField
# from embed_video.fields import EmbedVideoField
from rest_framework import serializers
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import math, random
import requests
import os
from rest_framework.decorators import action
from twilio.rest import Client, TwilioIpMessagingClient
from myapp.utils import create_new_ref_number, dt, otplogin
from datetime import date
# User._meta.get_field('email')._unique = True


device_categories = (
    (1, u'Fan'),
    (2, u'Light'),
    (3, u'Plug'),
    (4, u'TV'),
    (5, u'Gyeser'),
    (6, u'Others'),
    # (7, u'')
)


smart_device = (
    (1, u'Yes'),
    (2, u'No'),
)


class place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_id = models.CharField(max_length = 10,blank=False,unique=True,primary_key=True,default=create_new_ref_number)
    p_type = models.CharField(max_length=15)

class floor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_id = models.ForeignKey(place, max_length=10, null=False, default=1,on_delete=models.CASCADE)
    f_id = models.CharField(max_length = 10, blank=False,unique=True,primary_key=True,default=create_new_ref_number)
    f_name = models.CharField(max_length=15)

class flat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_id = models.ForeignKey(floor, max_length=10, null=False, default=1,on_delete=models.CASCADE)
    flt_id = models.CharField(max_length = 10, blank=False,unique=True,primary_key=True,default=create_new_ref_number)
    flt_name = models.CharField(max_length=15)
    

class room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flt_id = models.ForeignKey(flat, max_length=10, null=False, default=1, on_delete=models.CASCADE)
    r_id = models.CharField(max_length = 10,blank=False,unique=True,primary_key=True,default=create_new_ref_number)
    r_name = models.CharField(max_length=15)

class allDevices(models.Model):
    d_id = models.CharField(max_length=40, default=0,primary_key=True)

class device(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    r_id = models.ForeignKey(room, on_delete=models.CASCADE)
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE)
    date_installed = models.DateField(default=dt)

class deviceStatus(models.Model):
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE,primary_key=True)
    pin1Status = models.IntegerField(blank=True,null=True)
    pin2Status = models.IntegerField(blank=True,null=True)
    pin3Status = models.IntegerField(blank=True,null=True)
    pin4Status = models.IntegerField(blank=True,null=True)
    pin5Status = models.IntegerField(blank=True,null=True)
    pin6Status = models.IntegerField(blank=True,null=True)
    pin7Status = models.IntegerField(blank=True,null=True)
    pin8Status = models.IntegerField(blank=True,null=True)
    pin9Status = models.IntegerField(blank=True,null=True)
    pin10Status = models.IntegerField(blank=True,null=True)
    pin11Status = models.IntegerField(blank=True,null=True)
    pin12Status = models.IntegerField(blank=True,null=True)
    pin13Status = models.IntegerField(blank=True,null=True)
    pin14Status = models.IntegerField(blank=True,null=True)
    pin15Status = models.IntegerField(blank=True,null=True)
    pin16Status = models.IntegerField(blank=True,null=True)
    pin17Status = models.IntegerField(blank=True,null=True)
    pin18Status = models.IntegerField(blank=True,null=True)
    pin19Status = models.CharField(blank=True,null=True,max_length=100)
    pin20Status = models.CharField(blank=True,null=True,max_length=100)


class sensors(models.Model):
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE,primary_key=True)
    sensor1 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor2 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor3 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor4 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor5 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor6 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor7 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor8 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor9 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)
    sensor10 = models.FloatField(unique = False, max_length=50,default=0.0, blank=True)

class ssidPassword(models.Model):
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE,primary_key=True)
    ssid1 = models.CharField(unique=True, max_length=15,blank=True)
    password1 = models.CharField(null=False, max_length=50,blank=True)
    ssid2 = models.CharField(unique=True, max_length=15,blank=True)
    password2 = models.CharField(null=False, max_length=50,blank=True)
    ssid3 = models.CharField(unique=True, max_length=15,blank=True)
    password3 = models.CharField(null=False, max_length=50,blank=True)

class emergencyNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE,primary_key=True)
    number1 = models.CharField(null=True, max_length=12)
    number2 = models.CharField(null=True, max_length=12)
    number3 = models.CharField(null=True, max_length=12)
    number4 = models.CharField(null=True, max_length=12)
    number5 = models.CharField(null=True, max_length=12)

class pinName(models.Model):
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE,primary_key=True)
    pin1Name = models.CharField(blank=True,null=True,max_length=20)
    pin2Name = models.CharField(blank=True,null=True,max_length=20)
    pin3Name = models.CharField(blank=True,null=True,max_length=20)
    pin4Name = models.CharField(blank=True,null=True,max_length=20)
    pin5Name = models.CharField(blank=True,null=True,max_length=20)
    pin6Name = models.CharField(blank=True,null=True,max_length=20)
    pin7Name = models.CharField(blank=True,null=True,max_length=20)
    pin8Name = models.CharField(blank=True,null=True,max_length=20)
    pin9Name = models.CharField(blank=True,null=True,max_length=20)
    pin10Name = models.CharField(blank=True,null=True,max_length=20)
    pin11Name = models.CharField(blank=True,null=True,max_length=20)
    pin12Name = models.CharField(blank=True,null=True,max_length=20)
    pin13Name = models.CharField(blank=True,null=True,max_length=20)
    pin14Name = models.CharField(blank=True,null=True,max_length=20)
    pin15Name = models.CharField(blank=True,null=True,max_length=20)
    pin16Name = models.CharField(blank=True,null=True,max_length=20)
    pin17Name = models.CharField(blank=True,null=True,max_length=20)
    pin18Name = models.CharField(blank=True,null=True,max_length=20)
    pin19Name = models.CharField(blank=True,null=True,max_length=20)
    pin20Name = models.CharField(blank=True,null=True,max_length=20)


class pinschedule(models.Model):
    d_id = models.ForeignKey(allDevices, on_delete=models.CASCADE)
    date1 = models.DateField(default="2000-01-01",null=True)
    timing1 = models.TimeField(default='00:00')
    pin1Status = models.IntegerField(blank=True,null=True)
    pin2Status = models.IntegerField(blank=True,null=True)
    pin3Status = models.IntegerField(blank=True,null=True)
    pin4Status = models.IntegerField(blank=True,null=True)
    pin5Status = models.IntegerField(blank=True,null=True)
    pin6Status = models.IntegerField(blank=True,null=True)
    pin7Status = models.IntegerField(blank=True,null=True)
    pin8Status = models.IntegerField(blank=True,null=True)
    pin9Status = models.IntegerField(blank=True,null=True)
    pin10Status = models.IntegerField(blank=True,null=True)
    pin11Status = models.IntegerField(blank=True,null=True)
    pin12Status = models.IntegerField(blank=True,null=True)
    pin13Status = models.IntegerField(blank=True,null=True)
    pin14Status = models.IntegerField(blank=True,null=True)
    pin15Status = models.IntegerField(blank=True,null=True)
    pin16Status = models.IntegerField(blank=True,null=True)
    pin17Status = models.IntegerField(blank=True,null=True)
    pin18Status = models.IntegerField(blank=True,null=True)
    pin19Status = models.CharField(blank=True,null=True,max_length=100)
    pin20Status = models.CharField(blank=True,null=True,max_length=100)
   

class userimages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    images = models.ImageField(upload_to='profile_picture', blank=True)

class SomeModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    file = models.CharField(max_length=499999, blank=True)

class deviceIpAddress(models.Model):
    d_id = models.OneToOneField(allDevices, on_delete=models.CASCADE,primary_key=True)
    ipaddress = models.CharField(max_length=99,blank=True,null=True)


class subuseraccess(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    emailtest = EmailField()
    email = models.CharField(primary_key=True, max_length=100)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # p_id = models.ForeignKey(place, on_delete=models.CASCADE)
    # f_id = models.ForeignKey(floor, on_delete=models.CASCADE)

class subuserplace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    email = models.ForeignKey(subuseraccess, on_delete=models.CASCADE)
    p_id = models.ForeignKey(place, on_delete=models.CASCADE)



# class Profile(models.Model):
#     # user = models.OneToOneField(User ,on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=20)
#     otp = models.CharField(max_length=6)


# API for main user include all the parameters while creating new temporary user
# API for temporary user include only mobile or email with place, floor, room, device ID's

class tempuser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, blank=True)
    email = EmailField(blank=True)
    name = models.CharField(max_length=100,blank=False)
    date = models.DateField(default="2000-01-01",null=True)
    timing = models.TimeField(default='00:00')
    p_id = models.ForeignKey(place, on_delete=models.CASCADE, blank=True, null=True)
    f_id = models.ForeignKey(floor, on_delete=models.CASCADE, blank=True, null=True)
    flt_id = models.ForeignKey(flat, on_delete=models.CASCADE, blank=True, null=True)
    r_id = models.ForeignKey(room, on_delete=models.CASCADE, blank=True, null=True)
    d_id = models.ForeignKey(allDevices, on_delete=models.CASCADE, blank=True, null=True)

class tempUserVerification(models.Model):
    mobile = models.CharField(max_length=10, blank=False)
    # updated_date = models.DateField(auto_now_add=True)
    # updated_time = models.TimeField(auto_now=True,editable=True)
    otp = models.CharField(max_length=6, default=otplogin, blank=True)    

class otptemplogin(models.Model):
    mobile = models.CharField(max_length=10, blank=False)
    otp = models.CharField(max_length=6, blank=False)





# class Videos(models.Model):
#     video = EmbedVideoField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
