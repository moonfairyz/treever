from django import forms
from django.forms import ModelForm
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=100, required=True)
	last_name = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(max_length=254, help_text='eg. youremail@anyemail.com')

	class Meta:
		model = User
		fields = ('first_name','last_name','username','password1','password2')

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('name','description','image','latitude','longitude')
		
