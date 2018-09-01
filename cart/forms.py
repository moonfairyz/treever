from django import forms
from cart.models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = UserProfile
        widgets = {'user' : forms.HiddenInput()}