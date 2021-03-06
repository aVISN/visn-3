import os
from visn2 import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, FileResponse
from .models import *
from dashboard.forms import *

from django.contrib import messages

def filesView(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    search_text = request.GET.get('search_text')
    if search_text:
        files = ProjFile.objects.filter(author=request.user).filter(filename__contains=search_text).all()
    else:
        files = ProjFile.objects.filter(author=request.user).all()

    print(files)
    context['files'] = files

    users = User.objects.all()
    chat_form = MessageForm()
    context['target_users'] = users
    context['chat_form'] = chat_form
    if request.method == 'POST':
        f = MessageForm(request.POST)
        if f.is_valid():
            to_name = f.cleaned_data.get('mto')
            mto = User.objects.filter(username=to_name).first()
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()

    context['navbar'] = 'files'

    # # ------------- below was added to dashview -----------------------------
    contacts = []
    projects = Project.objects.all()
    freelancer = User.objects.filter(is_superuser = True)[0]

    # IF freelancer, add all users to contacts
    if(request.user == freelancer):
                for member in User.objects.all():
                    if(member != request.user):
                        contacts.append(member)

    #If not freelancer, only add freelancer and contacts from collective projects 
    else:                    
        for project in projects:
            members = project.members.all()
            foundMatch = False
            for member in members:
                if(member == request.user):
                    foundMatch = True
            if(foundMatch):
                for member in members:
                    if(member != request.user):
                        if member not in contacts:
                            contacts.append(member)

        if freelancer not in contacts:
            contacts.append(freelancer)    

    context['contacts'] = contacts
#####----------------------------------------------------------------------------------------------

    return render(request, 'files/files.html', context)


def newFile(request):
    context = {}
    users = User.objects.all()
    chat_form = MessageForm()
    context['target_users'] = users
    context['chat_form'] = chat_form
    if request.method == 'POST':
        f = MessageForm(request.POST)
        if f.is_valid():
            to_name = f.cleaned_data.get('mto')
            mto = User.objects.filter(username=to_name).first()
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()

    form = ProjFileForm(request.POST, request.FILES)
    if form.is_valid():
        print('bbb...')
        print(form.cleaned_data)
        p = ProjFile(project=form.cleaned_data.get('project'), 
            filename=form.cleaned_data.get('filename'),
            comment=form.cleaned_data.get('comment'),
            author=request.user)
        p.save()
        return redirect(reverse_lazy('files'))
    else:
        print('aaa....')
        for err in form.errors:
            print(err)

    form = ProjFileForm()
    context['form'] = form
    return render(request, 'files/new_file.html', context)


def file_response_download1(request, filepath):
    filepath = os.path.join(settings.MEDIA_ROOT, filepath)
    print(filepath)
    response = FileResponse(open(filepath, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + os.path.split(filepath)[-1]
    return response

def del_file(request, file_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    projfile = ProjFile.objects.filter(id=file_id).first()
    if not projfile:
        messages.info(request, 'no file!')   #success
        return redirect(reverse_lazy('files'))
    filepath = os.path.join(settings.MEDIA_ROOT, projfile.filename.name)
    print(filepath)
    projfile.delete()
    os.remove(filepath)
    return redirect(reverse_lazy('files'))
