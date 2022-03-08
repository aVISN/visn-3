from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# from matplotlib.pyplot import cla

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','id':'roundcorners','autocomplete':'off','required':'true'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','id':'roundcorners','autocomplete':'off','required':'true'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','id':'roundcorners','autocomplete':'off','required':'true'}),
            'email': forms.EmailInput(attrs={'class':'form-control','id':'roundcorners','autocomplete':'off','required':'true'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control','id':'roundcorners','autocomplete':'off','autofill':'off','required':'true'}),
            'password2': forms.TextInput(attrs={'class':'form-control','id':'roundcorners','autocomplete':'off','required':'true'}),
        }

class EmailForm(forms.Form):
    old_email = forms.EmailField(required=False, label='Old Email', max_length=100)
    new_email = forms.EmailField(required=True, label='New Email', max_length=100)