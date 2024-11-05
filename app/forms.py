from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=70, required=True)
    email = forms.EmailField(max_length=70, required=True, help_text='Insert a valid email address.')
    username = forms.CharField(max_length=70, required=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']