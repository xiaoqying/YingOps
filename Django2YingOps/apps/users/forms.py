from django import forms
from .models import *


class UserProfileForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,min_length=5)
    password = forms.CharField(required=True,max_length=20,min_length=5)


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    reg_email = forms.EmailField(required=True)
    reg_username = forms.CharField(required=True,min_length=5)
    reg_password = forms.CharField(required=True,min_length=5)
    rep_password = forms.CharField(required=True,min_length=5)
    phone = forms.CharField(required=True,min_length=11)
