# import pandas as pd
import smtplib

from django.http import response
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
from myapp.serializers import testimageSerializers,userSerializers,placeSerializers,floorSerializers,flatSerializers,roomSerializers,deviceSerializers,pinscheduleSerializers,pinscheduleTimeSerializers,deviceStatusSerializers,emernumberSerializers,sensorSerializers,ssidPasswordSerializers,pinnamesSerializers,userprofileimagesSerializers,deviceipaddressSerializers,subuseraccessSerializers,emailSerializers,subuseremailSerializers,subuserplaceSerializers,subuserplacegetSerializers,tempuserregisterSerializers,placenameSerializers,floornameSerializers,roomnameSerializers,otpfortampuserSerializers,otpuserloginSerializers,firstnameSerializers,flatSerializers,userlogingetdataSerializers,flatnameSerializers,dateasignSerializers,timeasignSerializers
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



                                            ##################### Device Pin Names ####################



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

@api_view(["GET","POST","PUT","DELETE"])
def pinscheduling(request):
    if request.method == "GET":
        device_data = pinschedule.objects.filter(user=request.user)
        schJson = pinscheduleSerializers(device_data, many=True)
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
        print('all set')
        try:
            print('excecuted')
            device_object=pinschedule.objects.get(d_id=device_id)
        except device_object.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = pinscheduleSerializers(device_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data updated", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        data1 = pinschedule.objects.all()
        data1Json = pinscheduleSerializers(data1, many=True)
        for data in data1Json.data:
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
            if (var1 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin1Status=request.GET['pin1Status'])
                device_data.delete()
            elif (var2 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin2Status=request.GET['pin2Status'])
                device_data.delete()
            elif (var3 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin3Status=request.GET['pin3Status'])
                device_data.delete()
            elif (var4 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin4Status=request.GET['pin4Status'])
                device_data.delete()
            elif (var5 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin5Status=request.GET['pin5Status'])
                device_data.delete()
            elif (var6 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin6Status=request.GET['pin6Status'])
                device_data.delete()
            elif (var7 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin7Status=request.GET['pin7Status'])
                device_data.delete()
            elif (var8 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin8Status=request.GET['pin8Status'])
                device_data.delete()
            elif (var9 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin9Status=request.GET['pin9Status'])
                device_data.delete()
            elif (var10 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin10Status=request.GET['pin10Status'])
                device_data.delete()
            elif (var11 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin11Status=request.GET['pin11Status'])
                device_data.delete()
            elif (var12 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin12Status=request.GET['pin12Status'])
                device_data.delete()
            elif (var13 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin13Status=request.GET['pin13Status'])
                device_data.delete()
            elif (var14 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin14Status=request.GET['pin14Status'])
                device_data.delete()
            elif (var15 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin15Status=request.GET['pin15Status'])
                device_data.delete()
            elif (var16 != None):
                device_data = pinschedule.objects.filter(user = request.GET['user'], date1=request.GET['date1'], timing1=request.GET['timing1'], pin16Status=request.GET['pin16Status'])
                device_data.delete()
        return Response("SCHEDULE Deleted.")


def scheduleT(request):
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
                    BASE_URL = f'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id={d_idvar}'#'https://genorion1.herokuapp.com/getpostdevicePinStatus/?d_id=DIDM12932021AAAAAA'
                    print("xxxxxxx1")
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var4}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var5}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var6}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var7}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var8}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var9}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var10}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var11}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var12}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var13}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var14}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var15}
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
                    token = "fc8a8de66981014125077cadbf12bb12cbfe95fb"

                    headers =  {'content-type' : 'application/json', 
                                'Authorization': "Token {}".format(token)}
                    data = {"put":"yes",'d_id':d_idvar,'pin1Status':var16}
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



                                    ############################ Profile photo  ###########################

                                    ###################### BASE 64 string ###################

                                    
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
        dd = list(nameJson.data)[0]["p_type"]
        print(dd)
        return Response(dd)

##### floor  #######

@api_view(["GET","POST"])
def floornamelist(request):
    if request.method == "GET":
        device_data = floor.objects.filter(f_id=request.GET['f_id'])
        nameJson = floornameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        dd = list(nameJson.data)[0]["f_name"]
        print(dd)
        return Response(dd)

##### flat  #######

@api_view(["GET","POST"])
def flatnamelist(request):
    if request.method == "GET":
        device_data = flat.objects.filter(flt_id=request.GET['flt_id'])
        nameJson = flatnameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        dd = list(nameJson.data)[0]["flt_name"]
        print(dd)
        return Response(dd)


##### room  #######

@api_view(["GET","POST"])
def roomnamelist(request):
    if request.method == "GET":
        device_data = room.objects.filter(r_id=request.GET['r_id'])
        nameJson = roomnameSerializers(device_data, many=True)
        # return Response(nameJson.data)
        dd = list(nameJson.data)[0]["r_name"]
        print(dd)
        return Response(dd)

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

