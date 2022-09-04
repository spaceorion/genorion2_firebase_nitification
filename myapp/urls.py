from django.urls import path,include
from django.conf import settings
from . import views
from . views import *
# from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('loatt' , views.login_attempt , name="login"),
    # path('register' , views.register , name="register"),
    # path('otp' , views.otp , name="otp"),
    # path('login-otp', views.login_otp , name="login_otp"),
    # path('',views.tempo,name="testing"),
    path('', views.index, name='homepage'),
    path('about', views.about, name='about-us'),
    path('contact', views.contact, name='contact-us'),
    path('product', views.product, name='ourproducts'),
    path('ourteam', views.ourteam, name='team'),
    path('sendmultiemail', views.testemail, name='testemail'),
    path('user', views.user, name='login'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('usersignup', views.usersignup, name='usersignup'),
    path('buy', views.buy, name='buy'),
    path('join', views.join, name='join us'),
    path('ui', views.ui, name='applikeui'),
    path('logout', views.logout, name='logout'),
    # path('thanks', views.thankyou,name='thankyoupage'),
    # path('test', views.test, name='testing'),
    path('index/', views.index, name='index'),
    path('regflu',views.register_flutter,name='flutter-register'),
    path('checkemail',views.checkemail,name='email-check'),
    path('checkpassword',views.checkpassword,name='pass-check'),
    path('subuserregister',views.subuser_register_flutter,name='subuser-flutter-register'),
    path('checksubusermail',views.checksubemail,name='subuser-email-check'),
    path('checksubuserpassword',views.checksubpassword,name='subuser-pass-check'),
    # path('validate_phone/',views.ValidatePhoneSendOTP,name='otp'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name='password_reset_complete'),
    path('change_password/', views.change_pass, name='change_password'),
    path('change_password_phone/', views.change_passwo, name='change_password'),
    path('flutter_change_password_login', views.flutter_change_password_login, name='flutter_change_password_login'),
    path('change_password_flu/', views.change_pass, name='change_password'),
    path('schedulepinstimes/', views.scheduleT, name='scheduling'),

    ##### schedule it  ########

    path('schedulebillprediction/', views.addallList, name='addalllist'),
    path('schedulebillpredictionday/', views.oneyearList, name='oneyearlist'),
    path('schedulebillpredictionyear/', views.threeYlist, name='Tyearlist'),



]