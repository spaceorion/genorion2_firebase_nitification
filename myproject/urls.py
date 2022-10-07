"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.urlpatterns import format_suffix_patterns
from myapp import views
from myapp import views as myapp_view
from myapp.views import enerzyList, pertenminute, scheduleT
from django.contrib.auth import views as auth
from .router import router
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),

    ######### api path ##########################

    path('api/',include(router.urls)),
    path('api-token-auth/',views.obtain_auth_token,name='api-tokn-auth'),


    path('getthedataofuser/',myapp_view.userdataList),

    ################       user related path         ##########################
    # path('login/',myapp_view.Login,name='login'),
    # path('logout/',auth.LogoutView.as_view(template_name='user/index.html'),name='logout'),
    # path('register/',myapp_view.register,name='register'),
    path('addyourplace/',myapp_view.placeList),
    path('addyourfloor/',myapp_view.floorList),
    path('addyourflat/',myapp_view.flatList),
    path('addroom/', myapp_view.roomList),
    path('addyourdevice/', myapp_view.deviceList),
    path('schedulingpinsalltheway/',myapp_view.pinscheduling),
    path('scheduledatagetbyid/', myapp_view.pinschedulingdevice),
    

    path('getallplaces/', myapp_view.placegetList),
    path('getallfloors/', myapp_view.floorgetList),
    path('getallflats/', myapp_view.flatgetList),
    path('getallrooms/', myapp_view.roomgetList),
    path('getalldevices/', myapp_view.devicegetList),
    
    path('getallplacesbyonlyplaceidp_id/', myapp_view.placegetallList),
    path('getallfloorsbyonlyplaceidp_id/', myapp_view.floorgetallList),
    path('getallflatbyonlyflooridf_id/', myapp_view.flatgetallList),
    path('getallroomsbyonlyflooridf_id/', myapp_view.roomgetallList),
    path('getalldevicesbyonlyroomidr_id/', myapp_view.devicegetallList),
    
    path('getpostdevicePinStatus/', myapp_view.devicePinStatus),
    path('webhookapi/', myapp_view.webhook),
    # path('getpostemergencynumber/', myapp_view.emerNumber),
    path('tensensorsdata/', myapp_view.sensorsList),
    # path('ssidpassword/', myapp_view.ssidList),
    path('editpinnames/', myapp_view.devicePinNames),
    path('addprofileimage/', myapp_view.profoto),
    path('addipaddress/', myapp_view.ipaddressList),
    path('subuseraccess/', myapp_view.subuaccess),
    path('subuserpalceaccess/', myapp_view.subuplace),
    path('subuserfindall/', myapp_view.subuserfind),
    path('subfindsubdata/', myapp_view.subuserfindsubuser),

    path('getuid/', myapp_view.useridList),
    path('notification/', myapp_view.fire),

###############  Getting Names    ####################
    path('getyouplacename/', myapp_view.placenamelist),
    path('getyoufloorname/', myapp_view.floornamelist),
    path('getyouflatname/', myapp_view.flatnamelist),
    path('getyouroomname/', myapp_view.roomnamelist),
    path('scenedetail/', myapp_view.SceneDetail),
    path('scenedevice/', myapp_view.ScenedeviceDetail),





########## for main user to get the list of subuser  ##############
    path('getalldatayouadded/', myapp_view.subuplaceget),

########## for main user to get the list of temporary user  ##############
    path('getalldatayouaddedtempuser/', myapp_view.tempulist),

######### tamporary user otp login #######################

    path('giveaccesstotempuser/', myapp_view.tempU),
    path('loginotpsend/', myapp_view.tempu),
    path('tempuserloginwithotp/', myapp_view.tempulogin),
    path('tempuserautodelete/', myapp_view.tempuserautodelete),

    ###### Bill pridiction #############3

    path('energyconsume/', myapp_view.enerzyList),
    path('pertenminuteenergy/',myapp_view.pertenminute),
    path('perhourenergy/',myapp_view.perhour),
    path('perdaysenergy/',myapp_view.perday),
    path('peryearenergy/',myapp_view.peryear),






    # path('testkrlo/', myapp_view.my_django_view)

    path('testimages123/', myapp_view.testimages123),


    # path('user/',views.employeesList.as_view()),
    # path('firmwareupdate/', myapp_view.firmwareupdate),
    # path('firmwarecheck/', myapp_view.firmwarecheck),
]
urlpatterns +=staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# scheduleT(repeat=3,repeat_until=None)

