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
    name = forms.CharField(max_length=70, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 100%'}))
    email = forms.EmailField(max_length=70, required=True, help_text='Insert a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 100%'}))
    username = forms.CharField(max_length=70, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 100%'}))
    description = forms.CharField(max_length=100, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control',
               'style': 'resize: none; height: 60px; max-width: 100%',
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
    
class ProductFilterForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search...'
    }))
    
    category = forms.ChoiceField(choices=[('', 'All Categories')], required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    min_price = forms.DecimalField(min_value=0, required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Min Price'
    }))
    
    max_price = forms.DecimalField(min_value=0, required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Max Price'
    }))
    
    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices += [(cat, cat) for cat in categories]