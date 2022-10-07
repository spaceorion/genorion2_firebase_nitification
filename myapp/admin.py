from django.contrib import admin
# Register your models here.
# from embed_video.admin import AdminVideoMixin
# from .models import Videos
# from .models import employees
from django.contrib import admin
from . models import *

admin.site.register(place)
admin.site.register(floor)
admin.site.register(flat)
admin.site.register(room)
admin.site.register(device)
admin.site.register(deviceStatus)
admin.site.register(sensors)
admin.site.register(scene)
admin.site.register(scene_devices)

admin.site.register(emergencyNumber)
admin.site.register(allDevices)
admin.site.register(ssidPassword)
admin.site.register(pinName)
admin.site.register(userimages)
admin.site.register(deviceIpAddress)
admin.site.register(subuseraccess)
admin.site.register(subuserplace)
admin.site.register(tempuser)
admin.site.register(tempUserVerification)
admin.site.register(otptemplogin)
admin.site.register(pinschedule)
admin.site.register(SomeModel)
admin.site.register(energy)
admin.site.register(oneHourEnergy)
admin.site.register(oneyeardata)
admin.site.register(threeyears)

admin.site.register(FirebaseDetails)



# class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
#     pass

# admin.site.register(Videos, MyModelAdmin)

# admin.site.register(employees)
