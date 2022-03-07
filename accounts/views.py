from distutils.log import error
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from .models import *
from .forms import CreateUserForm, EmailForm

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid Credentials')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('frontpage')


def passwordChange(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    errors = ''
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/')
        else:
            errors = form.errors
    form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form, 'err': errors})

def changeEmail(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    errors = ''
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            if request.user.email == form.cleaned_data.get('old_email'):
                request.user.email = form.cleaned_data.get('new_email')
                request.user.save()
            else:
                print('old_email:', request.user.email)
                errors = {'error':'old_email error!'}
        else:
            errors = form.errors
    form = EmailForm()
    return render(request, 'accounts/email_change.html', {'form': form, 'err': errors})
    

# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     fields = '__all__'
    # redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy('successLogin')


def postLoginView(request):
    return HttpResponse('view after success Login')
