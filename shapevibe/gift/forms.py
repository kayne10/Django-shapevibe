from django import forms
from django.contrib.auth.models import User

from .models import Gift

class GiftForm(forms.ModelForm):

    class Meta:
        model = Gift
        fields = ['gift_title', 'gift_description', 'gift_image']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
