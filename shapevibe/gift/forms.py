from django import forms
from django.forms import fields
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import Gift, Profile

class GiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GiftForm, self).__init__(*args, **kwargs)
        self.fields['price'].label = 'Price: Leave blank if gift is free.'
        self.fields['tags'].label = 'Tags: *Separate each value with comma. 5 max.'

    class Meta:
        model = Gift
        fields = ['gift_title', 'gift_description', 'gift_image', 'price', 'tags']


class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['tags'].label = 'Tags: *Separate each value with comma. 5 max.'

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'summary', 'avatar', 'tags')

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'auth-input'}),
        }