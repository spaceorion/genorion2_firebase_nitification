from myapp.models import userimages, tempUserVerification
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.forms import fields



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'email','phone_no','password1', 'password2','first_name','last_name']

class SubUserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2','first_name','last_name']

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')

class ImageForm(forms.ModelForm):
    class Meta:
        model = userimages
        fields = '__all__'

class TemporaryUserForm(forms.ModelForm):
    class Meta:
        model = tempUserVerification
        fields = '__all__'


# class TempUserOtpForm(forms.ModelForm):
#     class Meta:
#         model = tempUserVerification
#         fields = '__all__'

# class TempoForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'


