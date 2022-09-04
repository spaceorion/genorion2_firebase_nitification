from __future__ import absolute_import, unicode_literals
from celery import shared_task
# import pandas as pd
import smtplib

from django.http import response
from requests.api import request
from myapp.models import userimages
from myapp.models import ssidPassword
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework import status
# from .models import employees
# from .serializers import employeesSerializer
from django.shortcuts import get_object_or_404
# from myapp.models import Videos
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, SubUserRegisterForm, PasswordChangeForm, PasswordChangingForm, ImageForm,TemporaryUserForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, context
from myapp.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
# from myapp.serializers import testimageSerializers,userSerializers,placeSerializers,floorSerializers,flatSerializers,roomSerializers,deviceSerializers,pinscheduleSerializers,pinscheduleTimeSerializers,deviceStatusSerializers,emernumberSerializers,sensorSerializers,ssidPasswordSerializers,pinnamesSerializers,userprofileimagesSerializers,deviceipaddressSerializers,subuseraccessSerializers,emailSerializers,subuseremailSerializers,subuserplaceSerializers,subuserplacegetSerializers,tempuserregisterSerializers,placenameSerializers,floornameSerializers,roomnameSerializers,otpfortampuserSerializers,otpuserloginSerializers,firstnameSerializers,flatSerializers,userlogingetdataSerializers,flatnameSerializers,dateasignSerializers,timeasignSerializers, energySerializers, onehourenSerializers
from myapp.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import serializers
from rest_framework import status
import random, math
from datetime import date
import json
import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions
import http.client
import ast
from twilio.rest import Client
from myapp import utils
from myapp.utils import get_variable
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
import time
# from background_task import background


conn = http.client.HTTPConnection("2factor.in")

# Create your views here.

@api_view(["GET","POST","PUT"])
def userdataList(request):
    if request.method=="GET":
        device_data = User.objects.filter(id=request.GET['id'])
        nameJson = userlogingetdataSerializers(device_data, many=True)
        # return Response(nameJson.data)
        dd = list(nameJson.data)[0]
        print(dd)
        return Response(dd)


    # elif request.method == "POST":
    #     received_json_data=json.loads(request.body)
    #     serializer = floorSerializers(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(get_variable(), status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == "PUT":
    #     received_json_data=json.loads(request.body)
    #     device_id=received_json_data['f_id']
    #     try:
    #         device_object=floor.objects.get(f_id=device_id)
    #     except device_object.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     serializer = floorSerializers(device_object, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response("data updated", status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###################################################################################
########################## Flutter API ############################################

@csrf_exempt
# @renderer_classes((JSONRenderer))
def register_flutter(request):
    form = UserRegisterForm(request.POST)
    # print(request.POST)
    # print(form)
    if form.is_valid():
        form.save()
        return JsonResponse({"Registration":"Done"})
    else :
        # return JsonResponse({"Password is too similar"})
        print(form.errors.as_json())
        # return JsonResponse({"Password is too similar"})
        # return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR ,data=form.errors.as_json())
        # print("pass is too similar")
        # return JsonResponse({"Password is too similar"})

@csrf_exempt
# @renderer_classes((JSONRenderer))
def checkemail(request):
    email = request.POST['email']

    try:
        match = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'Exists':False})

    return JsonResponse({'Exists':True})

@csrf_exempt
# @renderer_classes((JSONRenderer))
def checkpassword(request):
    pas = request.POST['pass']

    try:
        password_validation.validate_password(pas)
        return JsonResponse({'valid':True})
    except:
        return JsonResponse({'valid':False})



#######################subuser register###############################


@csrf_exempt
# @renderer_classes((JSONRenderer))
def subuser_register_flutter(request):
    form = SubUserRegisterForm(request.POST)
    # print(request.POST)
    # print(form)
    if form.is_valid():
        form.save()
        return JsonResponse({"Registration":"Successful"})
    else :
        print(form.errors.as_json())
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR ,data=form.errors.as_json())

@csrf_exempt
# @renderer_classes((JSONRenderer))
def checksubemail(request):
    email = request.POST['email']

    try:
        match = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'Exists':False})

    return JsonResponse({'Exists':True})

@csrf_exempt
# @renderer_classes((JSONRenderer))
def checksubpassword(request):
    pas = request.POST['pass']

    try:
        password_validation.validate_password(pas)
        return JsonResponse({'valid':True})
    except:
        return JsonResponse({'valid':False})

                        ################### Change Password #####################

@login_required(login_url="/userlogin")
def change_pass(request):
    if request.method == "POST":
        frm = PasswordChangeForm(user=request.user, data=request.POST)
        if frm.is_valid():
            frm.save()
            return HttpResponseRedirect('/change_password')
    else:
        frm = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': frm})

@login_required(login_url="/flutter_change_password_login")
def change_passwo(request):
    if request.method == "POST":
        frm = PasswordChangeForm(user=request.user, data=request.POST)
        if frm.is_valid():
            frm.save()
            return HttpResponse("Password Changed", '/index')
    else:
        frm = PasswordChangeForm(user=request.user)
    return render(request, 'change_password_flu.html', {'form': frm})

def flutter_change_password_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/change_password_flu')
        else:
            messages.info(request,'invalid')
            return redirect('flutter_change_password_login')
    else:
        return render(request, 'flutter_change_password_login.html')




@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def useridList(request):
    if request.method=="GET":
        current_user = request.user
        print(current_user.id)
        return Response(current_user.id)


                        ############################# hardware apis ############################### 


                                        ###########   Add   place   #################


                                        
@api_view(["GET","POST","PUT","DELETE"])
# @permission_classes([IsAuthenticated])
def placeList(request):
    if request.method=="GET":
        data = place.objects.filter(user=request.user)
        placeJson = placeSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)
        # dd = placeJson.data[:]
        # return Response(dd[0])
    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = placeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_variable(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['p_id']
        try:
            device_object=place.objects.get(p_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = placeSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        data = place.objects.filter(p_id=request.GET['p_id'])
        # data2 = subuseraccess.objects.filter(email=request.GET['email'])
        # placeJson = subuserplaceSerializers(data, many=True)
        data.delete()
        # data2.delete()
        return Response("removed")

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def placegetList(request):
    if request.method=="GET":
        data = place.objects.filter(user = request.user)
        placeJson = placeSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)

           ################### Without security ###################################

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def placegetallList(request):
    if request.method=="GET":
        data = subuserplace.objects.filter(email=request.GET['email'])
        placeJson = subuserplacegetSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)



################ for subuser  #####################



                                ###########   Add   floor   #################


@api_view(["GET", "POST","PUT","DELETE"])
def floorList(request):
    if request.method=="GET":
        floor_data = floor.objects.filter(user = request.user,p_id=request.GET['p_id'])
        floorJson = floorSerializers(floor_data, many=True)
        # dd = floorJson.data[:]
        return Response(floorJson.data)

    
    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = floorSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_variable(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['f_id']
        try:
            device_object=floor.objects.get(f_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = floorSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        data = floor.objects.filter(f_id=request.GET['f_id'])
        # data2 = subuseraccess.objects.filter(email=request.GET['email'])
        # placeJson = subuserplaceSerializers(data, many=True)
        data.delete()
        # data2.delete()
        return Response("removed")

@api_view(["GET"])
def floorgetList(request):
    if request.method=="GET":
        floor_data = floor.objects.filter(user = request.user,p_id=request.GET['p_id'])
        floorJson = floorSerializers(floor_data, many=True)
        return Response(floorJson.data)

                ################### Without security ###################################

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def floorgetallList(request):
    if request.method=="GET":
        data = floor.objects.filter(p_id=request.GET['p_id'])
        placeJson = floorSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)



                                ###########   Add   floor   #################


@api_view(["GET", "POST","PUT","DELETE"])
def flatList(request):
    if request.method=="GET":
        flat_data = flat.objects.filter(user = request.user,f_id=request.GET['f_id'])
        flatJson = flatSerializers(flat_data, many=True)
        # dd = flatJson.data[:]
        return Response(flatJson.data)

    
    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = flatSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_variable(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['flt_id']
        try:
            device_object=flat.objects.get(flt_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = flatSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        data = flat.objects.filter(flt_id=request.GET['flt_id'])
        # data2 = subuseraccess.objects.filter(email=request.GET['email'])
        # placeJson = subuserplaceSerializers(data, many=True)
        data.delete()
        # data2.delete()
        return Response("removed")

@api_view(["GET"])
def flatgetList(request):
    if request.method=="GET":
        flat_data = flat.objects.filter(user = request.user,f_id=request.GET['f_id'])
        flatJson = flatSerializers(flat_data, many=True)
        return Response(flatJson.data)

                ################### Without security ###################################

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def flatgetallList(request):
    if request.method=="GET":
        data = flat.objects.filter(f_id=request.GET['f_id'])
        placeJson = flatSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)



                                ###########   Add   room   #################


@api_view(["GET","POST","PUT","DELETE"])
def roomList(request):
    if request.method=="GET":
        room_data = room.objects.filter(user = request.user,flt_id=request.GET['flt_id'])
        roomJson = roomSerializers(room_data, many=True)
        # rr = roomJson.data[:]
        return Response(roomJson.data)

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = roomSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_variable(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['r_id']
        try:
            device_object=room.objects.get(r_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = roomSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        data = room.objects.filter(r_id=request.GET['r_id'])
        # data2 = subuseraccess.objects.filter(email=request.GET['email'])
        # placeJson = subuserplaceSerializers(data, many=True)
        data.delete()
        # data2.delete()
        return Response("removed")

@api_view(["GET"])
def roomgetList(request):
    if request.method=="GET":
        room_data = room.objects.filter(user = request.user,flt_id=request.GET['flt_id'])
        roomJson = roomSerializers(room_data, many=True)
        return Response(roomJson.data)


                ################### Without security ###################################

@api_view(["GET"])
def roomgetallList(request):
    if request.method=="GET":
        room_data = room.objects.filter(flt_id=request.GET['flt_id'])
        roomJson = roomSerializers(room_data, many=True)
        return Response(roomJson.data)


                                ###########   Add Device      ################



@api_view(["GET","POST","DELETE"])
def deviceList(request):
    if request.method=="GET":
        room_data = device.objects.filter(user = request.user,r_id=request.GET['r_id'])
        roomJson = deviceSerializers(room_data, many=True)
        # rr = roomJson.data[:]
        return Response(roomJson.data)
    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = deviceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        data = device.objects.filter(r_id=request.GET['r_id'], d_id=request.GET['d_id'])
        # data2 = subuseraccess.objects.filter(email=request.GET['email'])
        # placeJson = subuserplaceSerializers(data, many=True)
        data.delete()
        # data2.delete()
        return Response("removed")

@api_view(["GET"])
def devicegetList(request):
    if request.method=="GET":
        room_data = device.objects.filter(user = request.user,r_id=request.GET['r_id'])
        devJson = deviceSerializers(room_data, many=True)
        return Response(devJson.data)


                ################### Without security ###################################

@api_view(["GET"])
def devicegetallList(request):
    if request.method=="GET":
        room_data = device.objects.filter(r_id=request.GET['r_id'])
        devJson = deviceSerializers(room_data, many=True)
        return Response(devJson.data)

                                ###########   Add   sensors   #################


@api_view(["GET","POST"])
def sensorsList(request):
    if request.method == "GET":
        device_data = sensors.objects.filter(d_id=request.GET['d_id'])
        roomJson = sensorSerializers(device_data, many=True)
        dd = roomJson.data[:]
        return Response(dd[0])

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        if received_json_data['put']!='yes':
            serializer = sensorSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data created", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            device_id=received_json_data['d_id']
            try:
                device_object=sensors.objects.get(d_id=device_id)
            except device_object.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = sensorSerializers(device_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data updated", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




                                ###########   PinStatus   #################




@api_view(["GET","POST"])
def devicePinStatus(request):
    if request.method == "GET":
        device_data = deviceStatus.objects.filter(d_id=request.GET['d_id'])
        roomJson = deviceStatusSerializers(device_data, many=True)
        dd = roomJson.data[:]
        return Response(dd[0])

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        if received_json_data['put']!='yes':
            serializer = deviceStatusSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data created", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            device_id=received_json_data['d_id']
            print('123')
            try:
                print('qwe')
                device_object=deviceStatus.objects.get(d_id=device_id)
            except device_object.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = deviceStatusSerializers(device_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data updated", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################### Update Pin Status For DilogFlow ###################################  OK GOOGLE  ######################

@api_view(["POST"])
def webhook(request):
    if request.method == "POST":
        req = json.loads(request.body)
        print(req)
        
        
        # action = req.get("queryResult").get("action")
        # d_id = req.get('queryresult').get('action')
        parameters = req.get("queryResult").get("parameters")
        # roomJson = deviceStatusSerializers(parameters, many=True)
        # device_id=req.get('queryresult').get('action')
        serializer = deviceStatusSerializers(data=parameters)
        # device_id=received_json_data['d_id']
        #     print('123')
        device_id=parameters['d_id']
        try:
            print('qwe')
            device_object=deviceStatus.objects.get(d_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = deviceStatusSerializers(device_object, data=parameters)
        # serializer = deviceStatusSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



                                            ######+en20+en30+############### Device Pin Names ####################



@api_view(["GET","POST","PUT"])
def devicePinNames(request):
    if request.method == "GET":
        device_data = pinName.objects.filter(d_id=request.GET['d_id'])
        roomJson = pinnamesSerializers(device_data, many=True)
        dd = roomJson.data[:]
        return Response(dd[0])

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = pinnamesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['d_id']
        print('all set')
        try:
            print('excecuted')
            device_object=pinName.objects.get(d_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = pinnamesSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ################# pin time Scheduling   #######################

@api_view(["GET"])
def pinschedulingdevice(request):
    if request.method == "GET":
        device_data = pinschedule.objects.filter(d_id=request.GET['d_id'])
        schJson = pinscheduleSerializers(device_data, many=True)
        return Response(schJson.data)


@api_view(["GET","POST","PUT","DELETE"])
def pinscheduling(request):
    if request.method == "GET":
        device_data = pinschedule.objects.filter(user=request.user)
        schJson = pinSerializers(device_data, many=True)
        return Response(schJson.data)

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = pinscheduleSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['d_id']
        id=received_json_data['id']
        
        print('all set')
        try:
            print('excecuted')
            device_object=pinschedule.objects.get(d_id=device_id,id=id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = pinscheduleSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        # data1 = pinschedule.objects.all()
        # data1Json = pinscheduleSerializers(data1, many=True)
        device_data = pinschedule.objects.filter(user = request.GET['user'], id=request.GET['id'])#d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin1Status=request.GET['pin1Status'])
        device_data.delete()
        # for data in data1Json.data:
        #     var1 = data['pin1Status']
        #     var2 = data['pin2Status']
        #     var3 = data['pin3Status']
        #     var4 = data['pin4Status']
        #     var5 = data['pin5Status']
        #     var6 = data['pin6Status']
        #     var7 = data['pin7Status']
        #     var8 = data['pin8Status']
        #     var9 = data['pin9Status']
        #     var10 = data['pin10Status']
        #     var11 = data['pin11Status']
        #     var12 = data['pin12Status']
        #     var13 = data['pin13Status']
        #     var14 = data['pin14Status']
        #     var15 = data['pin15Status']
        #     var16 = data['pin16Status']
        #     if (var1 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin1Status=request.GET['pin1Status'])
        #         device_data.delete()
        #     elif (var2 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin2Status=request.GET['pin2Status'])
        #         device_data.delete()
        #     elif (var3 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin3Status=request.GET['pin3Status'])
        #         device_data.delete()
        #     elif (var4 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin4Status=request.GET['pin4Status'])
        #         device_data.delete()
        #     elif (var5 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin5Status=request.GET['pin5Status'])
        #         device_data.delete()
        #     elif (var6 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin6Status=request.GET['pin6Status'])
        #         device_data.delete()
        #     elif (var7 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin7Status=request.GET['pin7Status'])
        #         device_data.delete()
        #     elif (var8 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin8Status=request.GET['pin8Status'])
        #         device_data.delete()
        #     elif (var9 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin9Status=request.GET['pin9Status'])
        #         device_data.delete()
        #     elif (var10 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin10Status=request.GET['pin10Status'])
        #         device_data.delete()
        #     elif (var11 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin11Status=request.GET['pin11Status'])
        #         device_data.delete()
        #     elif (var12 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin12Status=request.GET['pin12Status'])
        #         device_data.delete()
        #     elif (var13 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin13Status=request.GET['pin13Status'])
        #         device_data.delete()
        #     elif (var14 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin14Status=request.GET['pin14Status'])
        #         device_data.delete()
        #     elif (var15 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin15Status=request.GET['pin15Status'])
        #         device_data.delete()
        #     elif (var16 != None):
        #         device_data = pinschedule.objects.filter(user = request.GET['user'], d_id=request.GET['d_id'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin16Status=request.GET['pin16Status'])
        #         device_data.delete()
        #     else:
        #         return Response("Please Check details. Try Again!!!")
        
        return Response("SCHEDULE Deleted.")

# @background(schedule=5)
# @shared_task
# x = request
def scheduleT(request):
    print("going")
    now = datetime.now()
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    # second = '{:02d}'.format(now.second)
    day_month_year = '{}-{}-{}'.format(year, month, day)
    hour_minute_second = '{}:{}:00'.format(hour, minute)
    print(day_month_year)
    print(hour_minute_second)
    data1 = pinschedule.objects.all()
    data1Json = pinscheduleSerializers(data1, many=True)
    dataJson = pinscheduleTimeSerializers(data1, many=True)
    for data in data1Json.data:
        _date = data["date1"]
        _timing = data["timing1"]
        _id = data['id']
        var1 = data['pin1Status']
        var2 = data['pin2Status']
        var3 = data['pin3Status']
        var4 = data['pin4Status']
        var5 = data['pin5Status']
        var6 = data['pin6Status']
        var7 = data['pin7Status']
        var8 = data['pin8Status']
        var9 = data['pin9Status']
        var10 = data['pin10Status']
        var11 = data['pin11Status']
        var12 = data['pin12Status']
        var13 = data['pin13Status']
        var14 = data['pin14Status']
        var15 = data['pin15Status']
        var16 = data['pin16Status']
        d_idvar = data['d_id']
        print(var1)
        print(var2)
        print(_date)
        print(_timing)
        print("asdff",d_idvar)

        if _date<=day_month_year and _timing<=hour_minute_second:
            print("nono1")
            if pinschedule.objects.filter(id=_id):
                print("nono2")
                if (var1 != None):
                    print("nono3")
                    BASE_URL = f'http://127.0.0.1:8000/getpostdevicePinStatus/?d_id={d_idvar}'#'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id=DIDM12932021AAAAAA'
                    print("xxxxxxx1")
                    token = "07f6fc6f36a7f5205236496b9816c08db09c29e5"

                    headers =  {'content-type' : 'application/json',
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var1}
                    print("xxx1")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var2 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx2")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin2Status':var2}
                    print("xxx2")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx2")
                    auth_response.text
                    print(auth_response)
                    print("delete")
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var3 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx3")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin3Status':var3}
                    print("xxx3")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx3")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var4 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx4")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin4Status':var4}
                    print("xxx4")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx4")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var5 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin5Status':var5}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var6 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin6Status':var6}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var7 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin7Status':var7}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var8 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin8Status':var8}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var9 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin9Status':var9}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var10 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin10Status':var10}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var11 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin11Status':var11}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var12 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin12Status':var12}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var13 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin13Status':var13}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var14 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin14Status':var14}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var15 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin15Status':var15}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
                elif (var16 != None):
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'
                    print("xxxxxxx")
                    token = "774945db6cd2eec12fe92227ab9b811c888227c6"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin16Status':var16}
                    print("xxx")
                    auth_response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
                    print("xxergadfgx")
                    auth_response.text
                    print(auth_response)
                    data2 = pinschedule.objects.filter(id=_id)
                    print("matched")
                    data2.delete()
                    print("delete")
        else:
            print("not matched")
    return render(request,'scheduling.html')

# def backg_view(request):
#     while True:
#         scheduleT(repeat = 3)
#         return HttpResponse("running")
# new_year = datetime(2022, 7, 23)
# scheduleT(1, repeat=2,repeat_until=new_year)#some_id, 



                                ###########   Add  Emergency numbers   #################



@api_view(["GET","POST","PUT"])
def emerNumber(request):
    if request.method=="GET":
        enumdata = emergencyNumber.objects.filter(user = request.user,d_id=request.GET['d_id'])
        emernumberJson = emernumberSerializers(enumdata, many=True)
        dd = emernumberJson.data[:]
        return Response(dd[0])

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = emernumberSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method =="PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['d_id']
        try:
            device_object=emergencyNumber.objects.get(d_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = emernumberSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


                                ########### SSid Password #################


@api_view(["GET","POST","PUT"])
def ssidList(request):
    if request.method == "GET":
        device_data = ssidPassword.objects.filter(d_id=request.GET['d_id'])
        roomJson = ssidPasswordSerializers(device_data, many=True)
        dd = roomJson.data[:]
        return Response(dd[0])

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = ssidPasswordSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['d_id']
        try:
            device_object=ssidPassword.objects.get(d_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ssidPasswordSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


          ############### Bill pridiction API  ####################


oneHenergy = None
@api_view(["GET","POST","PUT"])
def enerzyList(request):
    if request.method == "GET":
        device_data = energy.objects.filter(d_id=request.GET['d_id'])
        enrJson = energySerializers(device_data, many=True)
        dd = enrJson.data[:]
        return Response(dd[0])
    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        if received_json_data['put']!='yes':
            serializer = energySerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data created", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            device_id=received_json_data['d_id']
            print('123')
            try:
                print('qwe')
                device_object=energy.objects.get(d_id=device_id)
            except device_object.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = energySerializers(device_object, data=request.data)
            # en60 = request.data['enrgy60']
            print("qeortupjg",serializer)
            # for no in serializer:
            #     eno60 = no['enrgy60']
            # print("60th",eno60)
            eno10 = request.data['enrgy10']
            # print(eno60, "yahi wala hai kya?")
            # xxyy = ''
            print(device_id)
            if energy.objects.filter(d_id=device_id).exists():
                device_data = energy.objects.filter(d_id=device_id)
                enrJson = energySerializers(device_data, many=True)
                dd = enrJson.data[:]
                # print("all data",dd)
                da = energy.objects.filter(d_id=device_id)
                daJson = energySerializers(da, many=True)
                for datahaha in daJson.data:
                    en10 = datahaha['enrgy10']
                    en20 = datahaha['enrgy20']
                    en30 = datahaha['enrgy30']
                    en40 = datahaha['enrgy40']
                    en50 = datahaha['enrgy50']
                    en60 = datahaha['enrgy60']
                    d_id = datahaha['d_id']
                    # givenD = datahaha['datee']
                    # givenT = datahaha['timinge']

# update now

                    t1 = energy.objects.get(d_id=d_id)
                    t1.enrgy60 = en50
                    t1.save()
                    t2 = energy.objects.get(d_id=d_id)
                    t2.enrgy50 = en40
                    t2.save()
                    t3 = energy.objects.get(d_id=d_id)
                    t3.enrgy40 = en30
                    t3.save()
                    t4 = energy.objects.get(d_id=d_id)
                    t4.enrgy30 = en20
                    t4.save()
                    t5 = energy.objects.get(d_id=d_id)
                    t5.enrgy20 = en10
                    t5.save()
                    t6 = energy.objects.get(d_id=d_id)
                    t6.enrgy10 = eno10
                    t6.save()
                    return Response("data updated", status=status.HTTP_201_CREATED)
#  comparing time
                    # now = datetime.now()
                    # year = '{:02d}'.format(now.year)
                    # month = '{:02d}'.format(now.month)
                    # day = '{:02d}'.format(now.day)
                    # hour = '{:02d}'.format(now.hour)
                    # minute = '{:02d}'.format(now.minute)
                    # # second = '{:02d}'.format(now.second)
                    # day_month_year = '{}-{}-{}'.format(year, month, day)
                    # # hour_minute_second = '{}:{}'.format(hour, minute)
                    # # print(hour % 12)
                    # print(minute)
                    # print(day_month_year)
                    # print("samay", givenT)
                    # h1 = int(hour) % 12
                    # m1 = int(minute)
                    # a, b, c = (givenT).split(":")
                    # h2 = int(a) % 12
                    # m2 = int(b)
                    # s2 = c
                    # t1 = h1 * 60 + m1 #current time
                    # t2 = h2 * 60 + m2 #given time
                    # print("current t",t1)
                    # print("given t2", t2)
                        
                    # # if (t1 == t2):
                    # #     print("Both are same times")
                    # # #return
                    # # else:
                            
                    #         # calculating the difference
                    # diff = t1-t2
                            
                    #     # calculating hours from
                    #     # difference
                    #     # h = (int(diff / 60)) % 24
                        
                    #     # calculating minutes from
                    #     # difference
                    # m = diff % 60

                    # print(":", m)

# @api_view(["GET","POST","PUT"])
def addallList(request):
    all_ids = energy.objects.all()
    # print(list(all_ids)[0].d_id.d_id)
    print(all_ids)
    for ID in list(all_ids):
        ID = ID.d_id.d_id
        print("sdfa",ID)
        h = oneHourEnergy.objects.filter(d_id=ID)
        hJson = onehourenSerializers(h, many=True)
        if oneHourEnergy.objects.filter(d_id=ID).exists():
            print("pass")
            pass
        else:
            hener = oneHourEnergy.objects.create(d_id=ID);
            hener.save();
        for h1 in hJson.data:
            he1 = h1['hour1']
            he2 = h1['hour2']
            he3 = h1['hour3']
            he4 = h1['hour4']
            he5 = h1['hour5']
            he6 = h1['hour6']
            he7 = h1['hour7']
            he8 = h1['hour8']
            he9 = h1['hour9']
            he10 = h1['hour10']
            he11 = h1['hour11']
            he12 = h1['hour12']
            he13 = h1['hour13']
            he14 = h1['hour14']
            he15 = h1['hour15']
            he16 = h1['hour16']
            he17 = h1['hour17']
            he18 = h1['hour18']
            he19 = h1['hour19']
            he20 = h1['hour20']
            he21 = h1['hour21']
            he22 = h1['hour22']
            he23 = h1['hour23']
            he24 = h1['hour24']
        # da = energy.objects.filter(d_id=request.GET['d_id'])
        da = energy.objects.filter(d_id=ID)
        daJson = energySerializers(da, many=True)
        for data in daJson.data:
            en10 = data['enrgy10']
            en20 = data['enrgy20']
            en30 = data['enrgy30']
            en40 = data['enrgy40']
            en50 = data['enrgy50']
            en60 = data['enrgy60']
            d_id = data['d_id']
            # Update energy10 with en20
            print(d_id)
            print(type(en10))
            def toFloat(x):
                try:
                    return float(x)
                except:
                    return 0
            global oneHenergy
            oneHenergy = toFloat(en10) + toFloat(en20) + toFloat(en30) + toFloat(en40) + toFloat(en50) + toFloat(en60)
            print(oneHenergy)
            # if oneHourEnergy.objects.filter(d_id=d_id).exists():
            #     print("pass")
            #     pass
            # else:
            #     hener = oneHourEnergy.objects.create(d_id=d_id);
            #     hener.save();
            #     print("hello")
            #     pass
            # HE = oneHourEnergy.objects.get(d_id=d_id)
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour24 = he23
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("1st hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour23 = he22
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("2nd hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour3=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour22 = he21
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("3rd hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour4=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour21 = he20
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("4th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour5=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour20 = he19
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("5th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour6=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour19 = he18
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("6th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour7=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour18 = he17
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("7th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour8=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour17 = he16
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("8th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour9=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour16 = he15
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("9th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour10=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour15 = he14
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("10th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour11=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour14 = he13
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("11th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour12=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour13 = he12
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("12th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour13=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour12 = he11
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("13th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour14=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour11 = he10
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("14th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour15=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour10 = he9
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("15th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour16=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour9 = he8
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("16th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour17=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour8 = he7
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("17th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour18=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour7 = he6
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("18th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour19=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour6 = he5
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("19th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour20=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour5 = he4
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("20th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour21=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour4 = he3
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("21st hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour22=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour3 = he2
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("22nd hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour23=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour2 = he1
            t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("23rd hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        #elif oneHourEnergy.objects.filter(d_id=d_id, hour24=0).exists():
            # print("I am in.")
            t = oneHourEnergy.objects.get(d_id=d_id)
            t.hour1 = oneHenergy
            t.save()
            
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #data1 = energy.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()

    return render(request, 'billprediction.html')

def oneyearList(request):    
    all_ids = energy.objects.all()
    # print(list(all_ids)[0].d_id.d_id)
    print(all_ids)
    for ID in list(all_ids):
        ID = ID.d_id.d_id
        print("sdfa",ID)
        h = oneyeardata.objects.filter(d_id=ID)
        hJson = oneyearenSerializers(h, many=True)
        if oneyeardata.objects.filter(d_id=ID).exists():
            print("pass")
            pass
        else:
            hener = oneyeardata.objects.create(d_id=ID);
            hener.save();
            print("hello")
        for yarr1 in hJson.data:
            yy1 = yarr1['day1']
            yy2 = yarr1['day2']
            yy3 = yarr1['day3']
            yy4 = yarr1['day4']
            yy5 = yarr1['day5']
            yy6 = yarr1['day6']
            yy7 = yarr1['day7']
            yy8 = yarr1['day8'] 
            yy9 = yarr1['day9']
            yy10 = yarr1['day10']
            yy11 = yarr1['day11']
            yy12 = yarr1['day12']
            yy13 = yarr1['day13']
            yy14 = yarr1['day14']
            yy15 = yarr1['day15']
            yy16 = yarr1['day16']
            yy17 = yarr1['day17']
            yy18 = yarr1['day18']
            yy19 = yarr1['day19']
            yy20 = yarr1['day20']
            yy21 = yarr1['day21']
            yy22 = yarr1['day22']
            yy23 = yarr1['day23']
            yy24 = yarr1['day24']
            yy25 = yarr1['day25']
            yy26 = yarr1['day26']
            yy27 = yarr1['day27']
            yy28 = yarr1['day28']
            yy29 = yarr1['day29']
            yy30 = yarr1['day30']
            yy31 = yarr1['day31']
            yy32 = yarr1['day32']
            yy33 = yarr1['day33']
            yy34 = yarr1['day34']
            yy35 = yarr1['day35']
            yy36 = yarr1['day36']
            yy37 = yarr1['day37']
            yy38 = yarr1['day38']
            yy39 = yarr1['day39']
            yy40 = yarr1['day40']
            yy41 = yarr1['day41']
            yy42 = yarr1['day42']
            yy43 = yarr1['day43']
            yy44 = yarr1['day44']
            yy45 = yarr1['day45']
            yy46 = yarr1['day46']
            yy47 = yarr1['day47']
            yy48 = yarr1['day48']
            yy49 = yarr1['day49']
            yy50 = yarr1['day50']
            yy51 = yarr1['day51']
            yy52 = yarr1['day52']
            yy53 = yarr1['day53']
            yy54 = yarr1['day54']
            yy55 = yarr1['day55']
            yy56 = yarr1['day56']
            yy57 = yarr1['day57']
            yy58 = yarr1['day58']
            yy59 = yarr1['day59']
            yy60 = yarr1['day60']
            yy61 = yarr1['day61']
            yy62 = yarr1['day62']
            yy63 = yarr1['day63']
            yy64 = yarr1['day64']
            yy65 = yarr1['day65']
            yy66 = yarr1['day66']
            yy67 = yarr1['day67']
            yy68 = yarr1['day68']
            yy69 = yarr1['day69']
            yy70 = yarr1['day70']
            yy71 = yarr1['day71']
            yy72 = yarr1['day72']
            yy73 = yarr1['day73']
            yy74 = yarr1['day74']
            yy75 = yarr1['day75']
            yy76 = yarr1['day76']
            yy77 = yarr1['day77']
            yy78 = yarr1['day78']
            yy79 = yarr1['day79']
            yy80 = yarr1['day80']
            yy81 = yarr1['day81']
            yy82 = yarr1['day82']
            yy83 = yarr1['day83']
            yy84 = yarr1['day84']
            yy85 = yarr1['day85']
            yy86 = yarr1['day86']
            yy87 = yarr1['day87']
            yy88 = yarr1['day88']
            yy89 = yarr1['day89']
            yy90 = yarr1['day90']
            yy91 = yarr1['day91']
            yy92 = yarr1['day92']
            yy93 = yarr1['day93']
            yy94 = yarr1['day94']
            yy95 = yarr1['day95']
            yy96 = yarr1['day96']
            yy97 = yarr1['day97']
            yy98 = yarr1['day98']
            yy99 = yarr1['day99']
            yy100 = yarr1['day100']
            yy101 = yarr1['day101']
            yy102 = yarr1['day102']
            yy103 = yarr1['day103']
            yy104 = yarr1['day104']
            yy105 = yarr1['day105']
            yy106 = yarr1['day106']
            yy107 = yarr1['day107']
            yy108 = yarr1['day108']
            yy109 = yarr1['day109']
            yy110 = yarr1['day110']
            yy111 = yarr1['day111']
            yy112 = yarr1['day112']
            yy113 = yarr1['day113']
            yy114 = yarr1['day114']
            yy115 = yarr1['day115']
            yy116 = yarr1['day116']
            yy117 = yarr1['day117']
            yy118 = yarr1['day118']
            yy119 = yarr1['day119']
            yy120 = yarr1['day120']
            yy121 = yarr1['day121']
            yy122 = yarr1['day122']
            yy123 = yarr1['day123']
            yy124 = yarr1['day124']
            yy125 = yarr1['day125']
            yy126 = yarr1['day126']
            yy127 = yarr1['day127']
            yy128 = yarr1['day128']
            yy129 = yarr1['day129']
            yy130 = yarr1['day130']
            yy131 = yarr1['day131']
            yy132 = yarr1['day132']
            yy133 = yarr1['day133']
            yy134 = yarr1['day134']
            yy135 = yarr1['day135']
            yy136 = yarr1['day136']
            yy137 = yarr1['day137']
            yy138 = yarr1['day138']
            yy139 = yarr1['day139']
            yy140 = yarr1['day140']
            yy141 = yarr1['day141']
            yy142 = yarr1['day142']
            yy143 = yarr1['day143']
            yy144 = yarr1['day144']
            yy145 = yarr1['day145']
            yy146 = yarr1['day146']
            yy147 = yarr1['day147']
            yy148 = yarr1['day148']
            yy149 = yarr1['day149']
            yy150 = yarr1['day150']
            yy151 = yarr1['day151']
            yy152 = yarr1['day152']
            yy153 = yarr1['day153']
            yy154 = yarr1['day154']
            yy155 = yarr1['day155']
            yy156 = yarr1['day156']
            yy157 = yarr1['day157']
            yy158 = yarr1['day158']
            yy159 = yarr1['day159']
            yy160 = yarr1['day160']
            yy161 = yarr1['day161']
            yy162 = yarr1['day162']
            yy163 = yarr1['day163']
            yy164 = yarr1['day164']
            yy165 = yarr1['day165']
            yy166 = yarr1['day166']
            yy167 = yarr1['day167']
            yy168 = yarr1['day168']
            yy169 = yarr1['day169']
            yy170 = yarr1['day170']
            yy171 = yarr1['day171']
            yy172 = yarr1['day172']
            yy173 = yarr1['day173']
            yy174 = yarr1['day174']
            yy175 = yarr1['day175']
            yy176 = yarr1['day176']
            yy177 = yarr1['day177']
            yy178 = yarr1['day178']
            yy179 = yarr1['day179']
            yy180 = yarr1['day180']
            yy181 = yarr1['day181']
            yy182 = yarr1['day182']
            yy183 = yarr1['day183']
            yy184 = yarr1['day184']
            yy185 = yarr1['day185']
            yy186 = yarr1['day186']
            yy187 = yarr1['day187']
            yy188 = yarr1['day188']
            yy189 = yarr1['day189']
            yy190 = yarr1['day190']
            yy191 = yarr1['day191']
            yy192 = yarr1['day192']
            yy193 = yarr1['day193']
            yy194 = yarr1['day194']
            yy195 = yarr1['day195']
            yy196 = yarr1['day196']
            yy197 = yarr1['day197']
            yy198 = yarr1['day198']
            yy199 = yarr1['day199']
            yy200 = yarr1['day200']
            yy201 = yarr1['day201']
            yy202 = yarr1['day202']
            yy203 = yarr1['day203']
            yy204 = yarr1['day204']
            yy205 = yarr1['day205']
            yy206 = yarr1['day206']
            yy207 = yarr1['day207']
            yy208 = yarr1['day208']
            yy209 = yarr1['day209']
            yy210 = yarr1['day210']
            yy211 = yarr1['day211']
            yy212 = yarr1['day212']
            yy213 = yarr1['day213']
            yy214 = yarr1['day214']
            yy215 = yarr1['day215']
            yy216 = yarr1['day216']
            yy217 = yarr1['day217']
            yy218 = yarr1['day218']
            yy219 = yarr1['day219']
            yy220 = yarr1['day220']
            yy221 = yarr1['day221']
            yy222 = yarr1['day222']
            yy223 = yarr1['day223']
            yy224 = yarr1['day224']
            yy225 = yarr1['day225']
            yy226 = yarr1['day226']
            yy227 = yarr1['day227']
            yy228 = yarr1['day228']
            yy229 = yarr1['day229']
            yy230 = yarr1['day230']
            yy231 = yarr1['day231']
            yy232 = yarr1['day232']
            yy233 = yarr1['day233']
            yy234 = yarr1['day234']
            yy235 = yarr1['day235']
            yy236 = yarr1['day236']
            yy237 = yarr1['day237']
            yy238 = yarr1['day238']
            yy239 = yarr1['day239']
            yy240 = yarr1['day240']
            yy241 = yarr1['day241']
            yy242 = yarr1['day242']
            yy243 = yarr1['day243']
            yy244 = yarr1['day244']
            yy245 = yarr1['day245']
            yy246 = yarr1['day246']
            yy247 = yarr1['day247']
            yy248 = yarr1['day248']
            yy249 = yarr1['day249']
            yy250 = yarr1['day250']
            yy251 = yarr1['day251']
            yy252 = yarr1['day252']
            yy253 = yarr1['day253']
            yy254 = yarr1['day254']
            yy255 = yarr1['day255']
            yy256 = yarr1['day256']
            yy257 = yarr1['day257']
            yy258 = yarr1['day258']
            yy259 = yarr1['day259']
            yy260 = yarr1['day260']
            yy261 = yarr1['day261']
            yy262 = yarr1['day262']
            yy263 = yarr1['day263']
            yy264 = yarr1['day264']
            yy265 = yarr1['day265']
            yy266 = yarr1['day266']
            yy267 = yarr1['day267']
            yy268 = yarr1['day268']
            yy269 = yarr1['day269']
            yy270 = yarr1['day270']
            yy271 = yarr1['day271']
            yy272 = yarr1['day272']
            yy273 = yarr1['day273']
            yy274 = yarr1['day274']
            yy275 = yarr1['day275']
            yy276 = yarr1['day276']
            yy277 = yarr1['day277']
            yy278 = yarr1['day278']
            yy279 = yarr1['day279']
            yy280 = yarr1['day280']
            yy281 = yarr1['day281']
            yy282 = yarr1['day282']
            yy283 = yarr1['day283']
            yy284 = yarr1['day284']
            yy285 = yarr1['day285']
            yy286 = yarr1['day286']
            yy287 = yarr1['day287']
            yy288 = yarr1['day288']
            yy289 = yarr1['day289']
            yy290 = yarr1['day290']
            yy291 = yarr1['day291']
            yy292 = yarr1['day292']
            yy293 = yarr1['day293']
            yy294 = yarr1['day294']
            yy295 = yarr1['day295']
            yy296 = yarr1['day296']
            yy297 = yarr1['day297']
            yy298 = yarr1['day298']
            yy299 = yarr1['day299']
            yy300 = yarr1['day300']
            yy301 = yarr1['day301']
            yy302 = yarr1['day302']
            yy303 = yarr1['day303']
            yy304 = yarr1['day304']
            yy305 = yarr1['day305']
            yy306 = yarr1['day306']
            yy307 = yarr1['day307']
            yy308 = yarr1['day308']
            yy309 = yarr1['day309']
            yy310 = yarr1['day310']
            yy311 = yarr1['day311']
            yy312 = yarr1['day312']
            yy313 = yarr1['day313']
            yy314 = yarr1['day314']
            yy315 = yarr1['day315']
            yy316 = yarr1['day316']
            yy317 = yarr1['day317']
            yy318 = yarr1['day318']
            yy319 = yarr1['day319']
            yy320 = yarr1['day320']
            yy321 = yarr1['day321']
            yy322 = yarr1['day322']
            yy323 = yarr1['day323']
            yy324 = yarr1['day324']
            yy325 = yarr1['day325']
            yy326 = yarr1['day326']
            yy327 = yarr1['day327']
            yy328 = yarr1['day328']
            yy329 = yarr1['day329']
            yy330 = yarr1['day330']
            yy331 = yarr1['day331']
            yy332 = yarr1['day332']
            yy333 = yarr1['day333']
            yy334 = yarr1['day334']
            yy335 = yarr1['day335']
            yy336 = yarr1['day336']
            yy337 = yarr1['day337']
            yy338 = yarr1['day338']
            yy339 = yarr1['day339']
            yy340 = yarr1['day340']
            yy341 = yarr1['day341']
            yy342 = yarr1['day342']
            yy343 = yarr1['day343']
            yy344 = yarr1['day344']
            yy345 = yarr1['day345']
            yy346 = yarr1['day346']
            yy347 = yarr1['day347']
            yy348 = yarr1['day348']
            yy349 = yarr1['day349']
            yy350 = yarr1['day350']
            yy351 = yarr1['day351']
            yy352 = yarr1['day352']
            yy353 = yarr1['day353']
            yy354 = yarr1['day354']
            yy355 = yarr1['day355']
            yy356 = yarr1['day356']
            yy357 = yarr1['day357']
            yy358 = yarr1['day358']
            yy359 = yarr1['day359']
            yy360 = yarr1['day360']
            yy361 = yarr1['day361']
            yy362 = yarr1['day362']
            yy363 = yarr1['day363']
            yy364 = yarr1['day364']
            yy365 = yarr1['day365']
            yy366 = yarr1['day366']

        yar = oneHourEnergy.objects.filter(d_id=ID)
        yarJson = onehourenSerializers(yar, many=True)
        for yoyo in yarJson.data:
            # en10 = data['enrgy10']           
            xc = yoyo["hour1"]
            xc2 = yoyo["hour2"]
            xc3 = yoyo["hour3"]
            xc4 = yoyo["hour4"]
            xc5 = yoyo["hour5"]
            xc6 = yoyo["hour6"]
            xc7 = yoyo["hour7"]
            xc8 = yoyo["hour8"]
            xc9 = yoyo["hour9"]
            xc10 = yoyo["hour10"]
            xc11 = yoyo["hour11"]
            xc12 = yoyo["hour11"]
            xc13 = yoyo["hour13"]
            xc14 = yoyo["hour14"]
            xc15 = yoyo["hour15"]
            xc16 = yoyo["hour16"]
            xc17 = yoyo["hour17"]
            xc18 = yoyo["hour18"]
            xc19 = yoyo["hour19"]
            xc20 = yoyo["hour20"]
            xc21 = yoyo["hour21"]
            xc22 = yoyo["hour22"]
            xc23 = yoyo["hour23"]
            xc24 = yoyo["hour24"]
            d_id = yoyo['d_id']
        
            def toFloat(x):
                try:
                    return float(x)
                except:
                    return 0

            xcall = toFloat(xc) + toFloat(xc2) + toFloat(xc3) + toFloat(xc4) + toFloat(xc5) + toFloat(xc6) + toFloat(xc7) + toFloat(xc8) + toFloat(xc9) + toFloat(xc10) + toFloat(xc11) + toFloat(xc12) + toFloat(xc13) + toFloat(xc14) + toFloat(xc15) + toFloat(xc16) + toFloat(xc17) + toFloat(xc18) + toFloat(xc19) + toFloat(xc20) + toFloat(xc21) + toFloat(xc22) + toFloat(xc23) + toFloat(xc24)
            print("one day Energy: ", xcall)

            t = oneyeardata.objects.get(d_id=d_id)
            t.day366 = yy365
            t.day365 = yy364
            t.day364 = yy363
            t.day363 = yy362
            t.day362 = yy361
            t.day361 = yy360
            t.day360 = yy359
            t.day359 = yy358
            t.day358 = yy357
            t.day357 = yy356
            t.day356 = yy355
            t.day355 = yy354
            t.day354 = yy353
            t.day353 = yy352
            t.day352 = yy351
            t.day351 = yy350
            t.day350 = yy349
            t.day349 = yy348
            t.day348 = yy347
            t.day347 = yy346
            t.day346 = yy345
            t.day345 = yy344
            t.day344 = yy343
            t.day343 = yy342
            t.day342 = yy341
            t.day341 = yy340
            t.day340 = yy339
            t.day339 = yy338
            t.day338 = yy337
            t.day337 = yy336
            t.day336 = yy335
            t.day335 = yy334
            t.day334 = yy333
            t.day333 = yy332
            t.day332 = yy331
            t.day331 = yy330
            t.day330 = yy329
            t.day329 = yy328
            t.day328 = yy327
            t.day327 = yy326
            t.day326 = yy325
            t.day325 = yy324
            t.day324 = yy323
            t.day323 = yy322
            t.day322 = yy321
            t.day321 = yy320
            t.day320 = yy319
            t.day319 = yy318
            t.day318 = yy317
            t.day317 = yy316
            t.day316 = yy315
            t.day315 = yy314
            t.day314 = yy313
            t.day313 = yy312
            t.day312 = yy311
            t.day311 = yy310
            t.day310 = yy309
            t.day309 = yy308
            t.day308 = yy307
            t.day307 = yy306
            t.day306 = yy305
            t.day305 = yy304
            t.day304 = yy303
            t.day303 = yy302
            t.day302 = yy301
            t.day301 = yy300
            t.day300 = yy299
            t.day299 = yy298
            t.day298 = yy297
            t.day297 = yy296
            t.day296 = yy295
            t.day295 = yy294
            t.day294 = yy293
            t.day293 = yy292
            t.day292 = yy291
            t.day291 = yy290
            t.day290 = yy289
            t.day289 = yy288
            t.day288 = yy287
            t.day287 = yy286
            t.day286 = yy285
            t.day285 = yy284
            t.day284 = yy283
            t.day283 = yy282
            t.day282 = yy281
            t.day281 = yy280
            t.day280 = yy279
            t.day279 = yy278
            t.day278 = yy277
            t.day277 = yy276
            t.day276 = yy275
            t.day275 = yy274
            t.day274 = yy273
            t.day273 = yy272
            t.day272 = yy271
            t.day271 = yy270
            t.day270 = yy269
            t.day269 = yy268
            t.day268 = yy267
            t.day267 = yy266
            t.day266 = yy265
            t.day265 = yy264
            t.day264 = yy263
            t.day263 = yy262
            t.day262 = yy261
            t.day261 = yy260
            t.day260 = yy259
            t.day259 = yy258
            t.day258 = yy257
            t.day257 = yy256
            t.day256 = yy255
            t.day255 = yy254
            t.day254 = yy253
            t.day253 = yy252
            t.day252 = yy251
            t.day251 = yy250
            t.day250 = yy249
            t.day249 = yy248
            t.day248 = yy247
            t.day247 = yy246
            t.day246 = yy245
            t.day245 = yy244
            t.day244 = yy243
            t.day243 = yy242
            t.day242 = yy241
            t.day241 = yy240
            t.day240 = yy239
            t.day239 = yy238
            t.day238 = yy237
            t.day237 = yy236
            t.day236 = yy235
            t.day235 = yy234
            t.day234 = yy233
            t.day233 = yy232
            t.day232 = yy231
            t.day231 = yy230
            t.day230 = yy229
            t.day229 = yy228
            t.day228 = yy227
            t.day227 = yy226
            t.day226 = yy225
            t.day225 = yy224
            t.day224 = yy223
            t.day223 = yy222
            t.day222 = yy221
            t.day221 = yy220
            t.day220 = yy219
            t.day219 = yy218
            t.day218 = yy217
            t.day217 = yy216
            t.day216 = yy215
            t.day215 = yy214
            t.day214 = yy213
            t.day213 = yy212
            t.day212 = yy211
            t.day211 = yy210
            t.day210 = yy209
            t.day209 = yy208
            t.day208 = yy207
            t.day207 = yy206
            t.day206 = yy205
            t.day205 = yy204
            t.day204 = yy203
            t.day203 = yy202
            t.day202 = yy201
            t.day201 = yy200
            t.day200 = yy199
            t.day199 = yy198
            t.day198 = yy197
            t.day197 = yy196
            t.day196 = yy195
            t.day195 = yy194
            t.day194 = yy193
            t.day193 = yy192
            t.day192 = yy191
            t.day191 = yy190
            t.day190 = yy189
            t.day189 = yy188
            t.day188 = yy187
            t.day187 = yy186
            t.day186 = yy185
            t.day185 = yy184
            t.day184 = yy183
            t.day183 = yy182
            t.day182 = yy181
            t.day181 = yy180
            t.day180 = yy179
            t.day179 = yy178
            t.day178 = yy177
            t.day177 = yy176
            t.day176 = yy175
            t.day175 = yy174
            t.day174 = yy173
            t.day173 = yy172
            t.day172 = yy171
            t.day171 = yy170
            t.day170 = yy169
            t.day169 = yy168
            t.day168 = yy167
            t.day167 = yy166
            t.day166 = yy165
            t.day165 = yy164
            t.day164 = yy163
            t.day163 = yy162
            t.day162 = yy161
            t.day161 = yy160
            t.day160 = yy159
            t.day159 = yy158
            t.day158 = yy157
            t.day157 = yy156
            t.day156 = yy155
            t.day155 = yy154
            t.day154 = yy153
            t.day153 = yy152
            t.day152 = yy151
            t.day151 = yy150
            t.day150 = yy149
            t.day149 = yy148
            t.day148 = yy147
            t.day147 = yy146
            t.day146 = yy145
            t.day145 = yy144
            t.day144 = yy143
            t.day143 = yy142
            t.day142 = yy141
            t.day141 = yy140
            t.day140 = yy139
            t.day139 = yy138
            t.day138 = yy137
            t.day137 = yy136
            t.day136 = yy135
            t.day135 = yy134
            t.day134 = yy133
            t.day133 = yy132
            t.day132 = yy131
            t.day131 = yy130
            t.day130 = yy129
            t.day129 = yy128
            t.day128 = yy127
            t.day127 = yy126
            t.day126 = yy125
            t.day125 = yy124
            t.day124 = yy123
            t.day123 = yy122
            t.day122 = yy121
            t.day121 = yy120
            t.day120 = yy119
            t.day119 = yy118
            t.day118 = yy117
            t.day117 = yy116
            t.day116 = yy115
            t.day115 = yy114
            t.day114 = yy113
            t.day113 = yy112
            t.day112 = yy111
            t.day111 = yy110
            t.day110 = yy109
            t.day109 = yy108
            t.day108 = yy107
            t.day107 = yy106
            t.day106 = yy105
            t.day105 = yy104
            t.day104 = yy103
            t.day103 = yy102
            t.day102 = yy101
            t.day101 = yy100
            t.day100 = yy99
            t.day99 = yy98
            t.day98 = yy97
            t.day97 = yy96
            t.day96 = yy95
            t.day95 = yy94
            t.day94 = yy93
            t.day93 = yy92
            t.day92 = yy91
            t.day91 = yy90
            t.day90 = yy89
            t.day89 = yy88
            t.day88 = yy87
            t.day87 = yy86
            t.day86 = yy85
            t.day85 = yy84
            t.day84 = yy83
            t.day83 = yy82
            t.day82 = yy81
            t.day81 = yy80
            t.day80 = yy79
            t.day79 = yy78
            t.day78 = yy77
            t.day77 = yy76
            t.day76 = yy75
            t.day75 = yy74
            t.day74 = yy73
            t.day73 = yy72
            t.day72 = yy71
            t.day71 = yy70
            t.day70 = yy69
            t.day69 = yy68
            t.day68 = yy67
            t.day67 = yy66
            t.day66 = yy65
            t.day65 = yy64
            t.day64 = yy63
            t.day63 = yy62
            t.day62 = yy61
            t.day61 = yy60
            t.day60 = yy59
            t.day59 = yy58
            t.day58 = yy57
            t.day57 = yy56
            t.day56 = yy55
            t.day55 = yy54
            t.day54 = yy53
            t.day53 = yy52
            t.day52 = yy51
            t.day51 = yy50
            t.day50 = yy49
            t.day49 = yy48
            t.day48 = yy47
            t.day47 = yy46
            t.day46 = yy45
            t.day45 = yy44
            t.day44 = yy43
            t.day43 = yy42
            t.day42 = yy41
            t.day41 = yy40
            t.day40 = yy39
            t.day39 = yy38
            t.day38 = yy37
            t.day37 = yy36
            t.day36 = yy35
            t.day35 = yy34
            t.day34 = yy33
            t.day33 = yy32
            t.day32 = yy31
            t.day31 = yy30
            t.day30 = yy29
            t.day29 = yy28
            t.day28 = yy27
            t.day27 = yy26
            t.day26 = yy25
            t.day25 = yy24
            t.day24 = yy23
            t.day23 = yy22
            t.day22 = yy21
            t.day21 = yy20
            t.day20 = yy19
            t.day19 = yy18
            t.day18 = yy17
            t.day17 = yy16
            t.day16 = yy15
            t.day15 = yy14
            t.day14 = yy13
            t.day13 = yy12
            t.day12 = yy11
            t.day11 = yy10
            t.day10 = yy9
            t.day9 = yy8
            t.day8 = yy7
            t.day7 = yy6
            t.day6 = yy5
            t.day5 = yy4
            t.day4 = yy3
            t.day3 = yy2
            t.day2 = yy1
            t.day1 = xcall
            t.save()
    return render(request, 'billpredictionday.html')
            # for i in range(1, 365+1):
            #     print("fghgfhdgdffgd", i)
            #     if oneyeardata.objects.filter(d_id=d_id, **{f'day{i}': None}).exists():
            #         print("I am in.", i)
            #         t = oneyeardata.objects.get(d_id=d_id)
            #         print('12121', xcall)
            #         setattr(t, f'day{i}', xcall)
            #         t.save()
            #         # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            #         # data1 = oneHourEnergy.objects.filter(d_id=request.GET['d_id'])
            #         #data1.delete()
            #         # return Response(f"day {i} Energy is: "+str(xcall), status=status.HTTP_201_CREATED)

            # if oneyeardata.objects.filter(d_id=d_id, **{f'day366': 0}).exists():
            #     print("I am in.", i)
            #     t = oneyeardata.objects.get(d_id=d_id)
            #     setattr(t, f'day366', xcall)
            #     t.save()
                # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
                # data1 = oneHourEnergy.objects.filter(d_id=request.GET['d_id'])
                #data1.delete()

def threeYlist(request):
    all_ids = energy.objects.all()
    # print(list(all_ids)[0].d_id.d_id)
    print(all_ids)
    for ID in list(all_ids):
        ID = ID.d_id.d_id
        print("sdfa",ID)
        h = oneyeardata.objects.filter(d_id=ID)
        hJson = oneyearenSerializers(h, many=True)
        if threeyears.objects.filter(d_id=ID).exists():
            print("pass")
            pass
        else:
            hener = threeyears.objects.create(d_id=ID);
            hener.save();
            print("hello")
        for yarr1 in hJson.data:
            d_id = yarr1['d_id']
        result = 0
        for i in range(1, 366+1):
            h1data = oneyeardata.objects.filter(d_id=d_id)
            subJson1 = oneyearenSerializers(h1data, many=True)
            xc = list(subJson1.data)[-1][f"day{i}"]
            def toFloat(x):
                try:
                    return float(x)
                except:
                    return 0
            result += toFloat(xc)
        print("one year energy", result)

        tyard = threeyears.objects.filter(d_id=ID)
        tyardJson = threeyearenSerializers(tyard, many=True)
        for tya in tyardJson.data:
            # en10 = data['enrgy10']           
            yaya1 = tya["year1"]
            yaya2 = tya["year2"]
            yaya3 = tya["year3"]
        
        # if threeyears.objects.filter(d_id=d_id, year1='').exists():
        #     print("I am in.")
        t = threeyears.objects.get(d_id=d_id)
        t.year3 = yaya2
        t.save()
        # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
        # data1 = oneyeardata.objects.filter(d_id=request.GET['d_id'])
        #data1.delete()
        # return Response("1st Year Energy is: "+str(result), status=status.HTTP_201_CREATED)
        # elif threeyears.objects.filter(d_id=d_id, year2='').exists():
        #     print("I am in.")
        t = threeyears.objects.get(d_id=d_id)
        t.year2 = yaya1
        t.save()
            # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
            # data1 = oneyeardata.objects.filter(d_id=request.GET['d_id'])
            #data1.delete()
            # return Response("2nd Year Energy is: "+str(result), status=status.HTTP_201_CREATED)
        # elif threeyears.objects.filter(d_id=d_id, year3='').exists():
        #     print("I am in.")
        t = threeyears.objects.get(d_id=d_id)
        t.year1 = result
        t.save()
                
                # oneHourEnergy.objects.filter(d_id=d_id).update(hour1=oneHenergy);
                # data1 = oneyeardata.objects.filter(d_id=request.GET['d_id'])
                #data1.delete()
                # return Response("3rd Year Energy is: "+str(result), status=status.HTTP_201_CREATED)
            # else:
                # return Response("not filled successfully", status=status.HTTP_100_CONTINUE)
                # return Response("24th hour Energy is: "+str(oneHenergy), status=status.HTTP_201_CREATED)
        # else:
        #     return Response("data updated", status=status.HTTP_201_CREATED)
    return render(request, 'billpredictionyear.html')
    


    

# if serializer.is_valid():
#     serializer.save()
    # return Response("data updated", status=status.HTTP_201_CREATED)
# if givenD<=day_month_year and givenT<=hour_minute_second:
# else:
# # def addthings(request):
#     return Response("data updated", status=status.HTTP_201_CREATED)
    
    # return render(request,'scheduling.html')
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                                    
@api_view(["GET"])
def pertenminute(request):
    if request.method == "GET":
        device_data = energy.objects.filter(d_id=request.GET['d_id'])
        enJson = energySerializers(device_data, many=True)
        # dd = roomJson.data[:]
        return Response(enJson.data)

@api_view(["GET"])
def perhour(request):
    if request.method == "GET":
        device_data = oneHourEnergy.objects.filter(d_id=request.GET['d_id'])
        enJson = onehourenSerializers(device_data, many=True)
        # dd = roomJson.data[:]
        return Response(enJson.data)

@api_view(["GET"])
def perday(request):
    if request.method == "GET":
        device_data = oneyeardata.objects.filter(d_id=request.GET['d_id'])
        enJson = oneyearenSerializers(device_data, many=True)
        # dd = roomJson.data[:]
        return Response(enJson.data)

@api_view(["GET"])
def peryear(request):
    if request.method == "GET":
        device_data = threeyears.objects.filter(d_id=request.GET['d_id'])
        enJson = threeyearenSerializers(device_data, many=True)
        # dd = roomJson.data[:]
        return Response(enJson.data)




            ############################ Profile photo  ###########################

                     ################### BASE 64 string ###################

                                    
@api_view(["GET","POST","PUT","DELETE"])
def testimages123(request):
    if request.method == "GET":
        device_data = SomeModel.objects.filter(user=request.user)
        roomJson = testimageSerializers(device_data, many=True)
        dd = roomJson.data[:]
        return Response(dd[0])

    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        serializer = testimageSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("image uploded.", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        received_json_data=json.loads(request.body)
        device_id=received_json_data['user']
        try:
            device_object=SomeModel.objects.get(user=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = testimageSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Pic updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        print("exc")
        device_data = SomeModel.objects.filter(user = request.GET['user'])
        device_data.delete()
        return Response("Image Deleted.")


                                    ############### In form data  #######################


@csrf_exempt
# @renderer_classes((JSONRenderer))
@api_view(["GET","POST","PUT","DELETE"])
def profoto(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
    # print(request.POST)
    # print(form)
        if form.is_valid():
            form.save()
            return JsonResponse({"Image Uploaded":"Successfully"})
        else :
        # return JsonResponse({"Password is too similar"})
            print(form.errors.as_json())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR ,data=form.errors.as_json())

    elif request.method == "GET":
        device_data = userimages.objects.filter(user = request.GET['user'])
        roomJson = userprofileimagesSerializers(device_data, many=True)
        dd = roomJson.data[:]
        print(dd)
        return Response(dd[0])

    elif request.method == "PUT":
        print("qwerty")
        device_data = userimages.objects.filter(user = request.GET['user'])
        device_data.delete()
        form = ImageForm(request.POST, request.FILES)
        # print(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            return JsonResponse({"Image Updated":"Successfully"})

####################    only update image without delete the orignal 1  #######################

        # mypic = userimages.objects.get(user=request.GET['user'])
        # print(mypic)
        # form = ImageForm(request.POST, request.FILES, instance=mypic)
        # if form.is_valid():
        #     form.save()
        #     return JsonResponse({"Image":"Updated"})
        # else :
        # # return JsonResponse({"Something went wrong"})
        #     print(form.errors.as_json())
        #     return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR ,data=form.errors.as_json())
    
    elif request.method == "DELETE":
        print("exc")
        device_data = userimages.objects.filter(user = request.GET['user'])
        device_data.delete()
        return Response("Image Deleted.")

                                ########################## Device IP Address  ##########################

@api_view(["GET","POST"])
def ipaddressList(request):
    if request.method == "GET":
        device_data = deviceIpAddress.objects.filter(d_id=request.GET['d_id'])
        roomJson = deviceipaddressSerializers(device_data, many=True)
        dd = roomJson.data[:]
        return Response(dd[0])
    elif request.method == "POST":
        received_json_data=json.loads(request.body)
        if received_json_data['put']!='yes':
            serializer = deviceipaddressSerializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data created", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            device_id=received_json_data['d_id']
            try:
                device_object=deviceIpAddress.objects.get(d_id=device_id)
            except device_object.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = deviceipaddressSerializers(device_object, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data updated", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET","POST","PUT","DELETE"])
def subuaccess(request):
    # if request.method=="GET":
    #     data = subuseraccess.objects.filter(user=request.user, p_id=request.GET['p_id'])
    #     placeJson = floorSerializers(data, many=True)
    #     print(data)
    #     return Response(placeJson.data)
    #     # return Response(device_data)

    if request.method == "POST":
        # received_json_data=json.loads(request.body)
        serializer = subuseraccessSerializers(data=request.data)
        # email12 = subuseraccess.objects.filter()
        # subJson1 = subuseremailSerializers(email12, many=True)
        # # success = False
        # for x in list(subJson1.data):
        #     xc = x["emailtest"]
        #     print(xc)
        # xc = ["emailtest"]
        # if User.objects.filter(email=xc).exists():
        #     print("ssucessss")
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response("data created", status=status.HTTP_201_CREATED)
        # email1 = subuseraccess.objects.filter(user=request.GET['user'])
        # email1 = "ppp@gm.com"
        # if User.objects.filter(email=email1).exists():
        # email = User.objects.filter(user=request.GET['email'])
        # if User.objects.get(user=request.GET['email']).exists():
        if serializer.is_valid():
            print("xtz")
            # email1 = "ppp@gm.com"
            # if User.objects.filter(email=email1).exists():
        # email1 = User.objects.get(user=request.GET['email'])
        # print(email1)
        # email1 = "pankajpalariya21@gmai.com"
        # email1 = request.POST['email']
            serializer.save()
            # email = subuseraccess.objects.filter(user=request.GET['email'])
            # print(email)
            email12 = subuseraccess.objects.filter()
            subJson1 = subuseremailSerializers(email12, many=True)
            success = False
            # for x in list(subJson1.data):
            xc = list(subJson1.data)[-1]["emailtest"]
            print(xc)
                # print(email12)
                # print(subJson1.data)
            if User.objects.filter(email=xc).exists():
                # user1 = User.objects.filter(name__contains='email')
                # user1 = User.objects.all()
                # print(user1)
                # userJson = userSerializers(user1, many=True)
                # main = list(userJson.data)
                # print(main)
                    # print(subuseraccess.emailtest)
                    # print(email)
                success = Response("email added as a SUB-USER", status=status.HTTP_201_CREATED)
            else:
                xcdelete = subuseraccess.objects.last()
                print(xcdelete)
                xcdelete.delete()
                return Response("Email not exists.")
            return success if success else Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        data = subuserplace.objects.filter(email=request.GET['email'], p_id=request.GET['p_id'])
        # data2 = subuseraccess.objects.filter(email=request.GET['email'])
        # placeJson = subuserplaceSerializers(data, many=True)
        data.delete()
        # data2.delete()
        return Response("removed")

########## for main user to get the list of subuser  ##############
@api_view(["GET"])
def subuplaceget(request):
    if request.method=="GET":
        data = subuserplace.objects.filter(user=request.user)
        placeJson = subuserplacegetSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)

@api_view(["GET"])
def subuserfind(request):
    if request.method=="GET":
        data = subuserplace.objects.filter(user=request.user)
        dataJson = subuserplaceSerializers(data, many=True)
        return Response(dataJson.data)

@api_view(["GET"])
def subuserfindsubuser(request):
    if request.method=="GET":
        data = subuserplace.objects.filter(email=request.GET['email'])
        dataJson = subuserplaceSerializers(data, many=True)
        return Response(dataJson.data)

@api_view(["GET","POST","PUT"])
def subuplace(request):
    if request.method=="GET":
        data = subuserplace.objects.filter(email=request.GET['email'])
        placeJson = subuserplacegetSerializers(data, many=True)
        print(data)
        return Response(placeJson.data)
        # return Response(device_data)

    elif request.method == "POST":
        # received_json_data=json.loads(request.body)
        serializer = subuserplaceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email1 = subuserplace.objects.filter()
            subJson1 = subuserplaceSerializers(email1, many=True)
            xc = list(subJson1.data)[-1]["p_id"]
            xc1 = list(subJson1.data)[-1]["email"]
            print(xc)
            return Response(xc+" Added to "+xc1, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

######################################  Getting Names      #################################

##### place  #######

@api_view(["GET","POST"])
def placenamelist(request):
    if request.method == "GET":
        device_data = place.objects.filter(p_id=request.GET['p_id'])
        nameJson = placenameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        # dd = list(nameJson.data)[0]["p_type"]
        # print(dd)
        return Response(nameJson.data)

##### floor  #######

@api_view(["GET","POST"])
def floornamelist(request):
    if request.method == "GET":
        device_data = floor.objects.filter(f_id=request.GET['f_id'])
        nameJson = floornameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        # dd = list(nameJson.data)[0]["f_name"]
        # print(dd)
        return Response(nameJson.data)

##### flat  #######

@api_view(["GET","POST"])
def flatnamelist(request):
    if request.method == "GET":
        device_data = flat.objects.filter(flt_id=request.GET['flt_id'])
        nameJson = flatnameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        # dd = list(nameJson.data)[0]["flt_name"]
        # print(dd)
        return Response(nameJson.data)


##### room  #######

@api_view(["GET","POST"])
def roomnamelist(request):
    if request.method == "GET":
        device_data = room.objects.filter(r_id=request.GET['r_id'])
        nameJson = roomnameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        # dd = list(nameJson.data)[0]["r_name"]
        # print(dd)
        return Response(nameJson.data)

################  User can get all data added by him  ####################
@api_view(["GET"])
def tempulist(request):
    if request.method == "GET":
        device_data = tempuser.objects.filter(user=request.user)
        nameJson = tempuserregisterSerializers(device_data, many=True)
        return Response(nameJson.data)

############### Registring temporary user by main user  ##############

                            ########## Auto delete Temporary User  ####################

@api_view(["DELETE"])
def tempuserautodelete(request):
    if request.method == "DELETE":
        now = datetime.now()
        year = '{:02d}'.format(now.year)
        month = '{:02d}'.format(now.month)
        day = '{:02d}'.format(now.day)
        hour = '{:02d}'.format(now.hour)
        minute = '{:02d}'.format(now.minute)
        # second = '{:02d}'.format(now.second)
        day_month_year = '{}-{}-{}'.format(year, month, day)
        hour_minute_second = '{}:{}:00'.format(hour, minute)
        print(day_month_year)
        print(hour_minute_second)
        data1 = tempuser.objects.all()
        dataJson = dateasignSerializers(data1, many=True)
        for data in dataJson.data:
            _date = data['date']
            _timing = data['timing']
            _id = data['id']
            print(_id)
            if day_month_year >= _date and hour_minute_second >= _timing:
                data2 = tempuser.objects.filter(id=_id)
                print("matched")
                data2.delete()  
                print("delete")        
            else:
                print("not matched")
        return render(request,'tempUdelete.html')





@api_view(["GET","POST","DELETE"])
def tempU(request):
    if request.method == "GET":
        device_data = tempuser.objects.filter(mobile=request.GET['mobile'])
        nameJson = tempuserregisterSerializers(device_data, many=True)
        return Response(nameJson.data)
    elif request.method == "POST":
        tempdata = tempuserregisterSerializers(data=request.data)
        if tempdata.is_valid():
            tempdata.save()
            return Response("Temporary User is now active.", status=status.HTTP_201_CREATED)
        return Response(tempdata.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        # received_json_data=json.loads(request.body)
        # if received_json_data['id']=='p_id':
        try:
            data = tempuser.objects.filter(mobile=request.GET['mobile'], p_id=request.GET['p_id'])
            #print(data)
            data.delete()
        except Exception:
            print("p_id not found")
            pass

        try:
        # elif received_json_data['id']=='f_id':
            data2 = tempuser.objects.filter(mobile=request.GET['mobile'], f_id=request.GET['f_id'])
            data2.delete()
        except Exception:
            print("f_id not found")
            pass
        # elif received_json_data['id']=='r_id':

        try:
            data3 = tempuser.objects.filter(mobile=request.GET['mobile'], r_id=request.GET['r_id'])
            data3.delete()
        
        # elif received_json_data['id']=='d_id':
        except Exception:
            print("r_id not found")
            pass
        try:
            data4 = tempuser.objects.filter(mobile=request.GET['mobile'], d_id=request.GET['d_id'])
            data4.delete()
        except Exception:
            print("d_id not found")
            pass

        # else:
        #     print("not found")
        # data2 = tempUserVerification.objects.filter(mobile=request.GET['mobile']) or tempUserVerification.objects.filter(email=request.GET['email'])
        # data3 = otptemplogin.objects.filter(mobile=request.GET['mobile']) or otptemplogin.objects.filter(email=request.GET['email'])
        # data2.delete()
        # data3.delete()
        return Response("Temporary User has no longer Exists.")



 #############################################################################################################################################                
 #############################################################################################################################################                
  

def firmwarecheck(request):
    return HttpResponse("2.3", content_type="text/plain")



# @api_view(["GET"])
def firmwareupdate(request):
    path = 'firmware.bin'
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    with open(file_path, 'rb') as f:
        body = f.read()
    response = HttpResponse(body,content_type='application/x-binary')
    response['Content-Disposition']= 'attachment; filename='+file_path
    return response



###################################        website urls          #####################################


def tempo(request):
    return render(request, 'tempo.html')
def about(request):
    # videos = Videos.objects.all()
    # context = {
    #     'videos' : videos

    #     }
    return render(request, 'about.html') #context
def contact(request):
    if request.method == "POST":
        namevar = request.POST['name']
        emailvar = request.POST['email']
        phonevar = request.POST['phone']
        messagevar = request.POST['message']

        all = "Name: "+namevar+os.linesep+os.linesep+"Email: "+emailvar+os.linesep+os.linesep+"Number: "+phonevar+os.linesep+os.linesep+"Message: "+os.linesep+"               ( "+messagevar+" )"
        send_mail('An Email has been received from website.',
         all,
        settings.EMAIL_HOST_USER,
        ['spaceorion2021@gmail.com'],
        fail_silently=False)
    return render(request, 'contact.html')
def product(request):
    return render(request, 'product.html')
def ourteam(request):
    # tempdata = tempuserregisterSerializers(data=request.data)
    device_data = room.objects.filter()
    nameJson = dateasignSerializers(device_data, many=True)
    # return Response(nameJson.data)
    dd = (nameJson.data)
    print(dd)
    return render(request, 'ourteam.html')
def user(request):
    return render(request, 'user.html')
def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/ui')
        else:
            messages.info(request,'invalid')
            return redirect('/userlogin')
    else:
        return render(request, 'userlogin.html')
def usersignup(request):
    now = datetime.now()
    date = now.strftime("%D")
    if request.method == 'POST':
        name1 = request.POST['first_name']
        name2 = request.POST['last_name']
        username = request.POST['email']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        # number = request.POST['number']
        if pass1==pass2:

            if User.objects.filter(email=email).exists():
                messages.info(request, 'Try with another Email...')
                return redirect('usersignup')
            else:
                # x = name1
                # j = 0
                # while User.objects.filter(username=x).exists():
                #     j += 1
                #     x = name1 +'.'+str(j)
                user = User.objects.create_user(first_name=name1, last_name=name2, password=pass1, email=email, username=email);
                user.save();
                # messages.info(request, 'Your Username is'+' '+'('+' '+email+' '+')')
                return redirect('/userlogin')
        else:
            messages.info(request, 'Password not matching...')
            return redirect('usersignup')
    else:
        return render(request, 'usersignup.html')
def buy(request):
    return render(request, 'buy.html')
def join(request):
    return render(request, 'join.html')
def index(request):
    return render(request, 'index.html')
def all(request):
    return render(request, 'all.html')
@login_required(login_url="/userlogin")
def ui(request):
    return render(request, 'ui.html')
def logout(request):
    auth.logout(request)
    return redirect('/userlogin')




def testemail(request):
    if request.method == "POST":
        name = User.objects.filter()
        nameJson = firstnameSerializers(name, many=True)
        # print(nameJson.data)
        names = []
        for y in nameJson.data:
            names.append(y["first_name"])
        print(names)
        alle = User.objects.filter()
        dataJson = emailSerializers(alle, many=True)
        emails = []
        for x in dataJson.data:
            emails.append(x["email"])
        # dd = list(map(lambda x: x["email"], dataJson.data))
        print(emails)
        # emails = emails
        
        length = len(names)
        i = 0
        while i<length:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("spaceorion2021@gmail.com", "space@2020@")
            msg = f"Hello, {names[i]}\nWe are glad to tell you that you are luckey winner."
            subject = f"Hello, {names[i]} an update form Genorion."
            body = "Subject: {}\n\n{}".format(subject,msg)
            print(names[i])
            print(emails[i])
            server.sendmail("spaceorion2021@gmail.com",emails[i], body)
            i += 1
            
        # for email in emails:
            
        server.quit()
        # namevar = request.POST['name']
        # emailvar = request.POST['email']
        # phonevar = request.POST['phone']
        # messagevar = request.POST['message']

        # all = "Name: "+namevar+os.linesep+os.linesep+"Email: "+emailvar+os.linesep+os.linesep+"Number: "+phonevar+os.linesep+os.linesep+"Message: "+os.linesep+"               ( "+messagevar+" )"
        # send_mail('An Email has been received from website.',
        #  all,
        # settings.EMAIL_HOST_USER,
        # ['spaceorion2021@gmail.com'],
        # fail_silently=False)
    return render(request, 'testemail.html')
# def test(request):
#     return render(request, 'test.html')

##### otp sending############

def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    x = otp
    y = mobile
    n = '+91'
    account_sid = 'ACd6173a93be390fe7eb1f2bf7faceeb0e'
    auth_token = '4892323294c8cc241e2107380b0c3f59'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body='Your OTP is ' + x + '. Please add this OTP to login field as directed.\n' + 'THANK YOU for using GENORION.',
                                from_='+12095887091',
                                to=n+y
                            )
    print(message.sid)
    print(x)
    # return super().save(*args, **kwargs)
    return None

############### form for enter mobile number for temporary user  #################
@api_view(["GET","POST","DELETE"])
def tempu(request):
    if request.method == "POST":
        form = TemporaryUserForm(request.POST)
    # print(request.POST)
    # print(form)
        if form.is_valid():
            form.save()
            number = tempUserVerification.objects.filter()
            subJson1 = otpfortampuserSerializers(number, many=True)
            # success = False
            # for x in list(subJson1.data):
            mobile1 = list(subJson1.data)[-1]["mobile"]
            otp = list(subJson1.data)[-1]["otp"]
            if tempuser.objects.filter(mobile=mobile1).exists():
                print(mobile1)
                print(otp)
                send_otp(mobile1, otp)
            # request.session['mobile'] = mobile
                return Response("Otp Sent to your mobile number.", status=status.HTTP_201_CREATED)
            else:
                deletetemp = tempUserVerification.objects.last()
                print(deletetemp)
                deletetemp.delete()
                return Response("number does not exists.")
        else :
        # return JsonResponse({"Password is too similar"})
            print(form.errors.as_json())
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR ,data=form.errors.as_json())

########## Temporary User get data and login ###################

@api_view(["GET","POST"])
def tempulogin(request):
    if request.method == "GET":
        data = tempuser.objects.filter(mobile=request.GET['mobile'])
        Jsondata = tempuserregisterSerializers(data, many=True)
        # dd0 = list(Jsondata.data)[0]["p_id"]
        # dd1 = list(Jsondata.data)[0]["f_id"]
        # dd2 = list(Jsondata.data)[0]["r_id"]
        # dd3 = list(Jsondata.data)[0]["d_id"]
        # dd4 = list(Jsondata.data)[0]["mobile"]
        # dd5 = list(Jsondata.data)[0]["email"]
        # dd = []
        # dd.extend((dd0,dd1,dd2,dd3,dd4,dd5))
        return Response(Jsondata.data)
    # mobile = request.session['mobile']
    # context = {'mobile':mobile}
    elif request.method == 'POST':
        serializer = otpuserloginSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = otptemplogin.objects.filter()
            Jsondata = otpfortampuserSerializers(data, many=True)
            mobile1 = list(Jsondata.data)[-1]["mobile"]
            otp1 = list(Jsondata.data)[-1]["otp"]
            if tempUserVerification.objects.filter(mobile=mobile1, otp=otp1).exists():
                print(otp1)
                return Response("Now you have the access.", status=status.HTTP_201_CREATED)
            else:
                data = otptemplogin.objects.last()
                data.delete()
                return Response("Otp not matching.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

