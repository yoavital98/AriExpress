from django import forms
from django.forms import ModelForm

from .models import Member , UserMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

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

class NominateUserForm(ModelForm):
    username = forms.CharField(max_length=100)
    CHOICES = (('Owner', 'Option 1'),('Manager', 'Option 2'),)
    field = forms.ChoiceField(choices=CHOICES)


class UserMessageform(forms.Form):
    sender = forms.CharField(max_length=50)
    file = forms.FileField(required=False)
    receiver = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    content = forms.CharField(max_length=1000)
    creation_date = forms.DateTimeField(required=False)
    status = forms.CharField(max_length=10)


class NewProductForm(forms.Form):
    productName = forms.CharField(max_length=100)
    productCategory = forms.CharField(max_length=100)
    productPrice = forms.IntegerField()
    productQuantity = forms.IntegerField()
    
# TODO: change name to something like BasketRemoveProductForm
class BasketRemoveProductForm(forms.Form):
    product_id = forms.IntegerField()
    store_name = forms.CharField(max_length=100)

# TODO: change name to something like BasketEditQuantityProductForm
class BasketEditProductForm(forms.Form):
    product_id = forms.IntegerField()
    store_name = forms.CharField(max_length=100)
    quantity = forms.IntegerField()

class BasketAddProductForm(forms.Form):
    product_id = forms.IntegerField()
    store_name = forms.CharField(max_length=100)
    quantity = forms.IntegerField()


class CheckoutForm(forms.Form):
    firstName = forms.CharField(max_length=100)
    lastName = forms.CharField(max_length=100)
    #email = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=100)
    cc_name = forms.CharField(max_length=100)
    cc_number = forms.CharField(max_length=16)
    cc_id = forms.CharField(max_length=9)
    cc_expiration = forms.CharField(max_length=7)
    cc_cvv = forms.CharField(max_length=3)

