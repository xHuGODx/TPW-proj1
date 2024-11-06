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

class UpdateUserProfileForm(forms.Form):
    name = forms.CharField(max_length=70, required=True)
    email = forms.EmailField(max_length=70, required=True, help_text='Insert a valid email address.')
    username = forms.CharField(max_length=70, required=True)
    description = forms.CharField(max_length=100, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control',
               'style': 'resize: none; height: 80px;',
               'placeholder': 'Tell us something about yourself...'}))

class UpdateUserImageForm(forms.Form):
    image = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control',
               'id': 'image',
               'name': 'input_file',
               'accept': 'image/*'
               }))
    
class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=70, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    new_password = forms.CharField(max_length=70, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(max_length=70, required=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))