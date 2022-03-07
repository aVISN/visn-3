# docs forms: https://docs.djangoproject.com/en/3.2/topics/forms/ 

from pyexpat import model
from statistics import mode
from xml.dom import ValidationErr
# from attr import attrs
from django import forms
from django.forms import widgets
# from django.contrib.auth.forms import UserCreationForm
from .models import *

# ModelForm: https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/

class ProjFileForm(forms.ModelForm):
    class Meta:
        model = ProjFile
        exclude = ['author', 'id']
    

class NewProjForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['create_user', ]
        
class MessageForm(forms.Form):
    mto = forms.CharField(min_length=5, label='to name', required=True, widget=forms.HiddenInput())
    message = forms.CharField(widget=widgets.Textarea(attrs={'rows': 1}), label='message text', required=True)

class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['id', 'status']
    # project = forms.ModelChoiceField(queryset=None)
    # form.fields['books'].queryset 


# class UploadForm(forms.ModelForm):
#     class Meta: 
#         model = Upload
#         fields = ('description', 'comments', 'filename')


# class MyUserForm(forms.Form):
#     name = forms.CharField(min_length=5, label='name', required=True)
#     password = forms.CharField(min_length=4, label='password', required=True)
#     password2 = forms.CharField(min_length=4, label='confirm password', required=True)
#     userType = forms.ChoiceField(choices=[(1,'client'), (2, 'programer')], label='user type')

#     def clean(self):
#         ps = self.cleaned_data.get('password')
#         ps2 = self.cleaned_data.get('password2')
#         if ps == ps2:
#             return self.cleaned_data
#         self.add_error('password2', ValidationErr('confirm password error!'))

# class LoginForm(forms.Form):
#     name = forms.CharField(min_length=5, label='name', required=True)
#     password = forms.CharField(min_length=4, label='password', required=True)

# class MyUserCreationForm(UserCreationForm):
#     userType = forms.ChoiceField(choices=[(1,'client'), (2, 'Freelancer')], label='user type', required=True)
    
#     class Meta(UserCreationForm.Meta):
#         model = DjUser
#         fields = ['username', 'password1', 'password2', 'userType']

