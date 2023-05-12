from django import forms
from django.forms import ModelForm
from .models import Member , UserMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class loginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

class Register(ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class CreateMemberForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserMessagesform(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = UserMessage
        fields = "__all__"