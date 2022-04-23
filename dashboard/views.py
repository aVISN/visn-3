import math
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.forms import model_to_dict
from .models import *
from .forms import *
from django.db.models import Q



def dashboardView(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    projects = Project.objects.filter(Q(create_user=request.user) | Q(members=request.user)).distinct()[:]
    res = []
    for i in range(math.ceil(len(projects)/3)):
        res.append(projects[i * 3: (i+1)*3])
    context['projects'] = res
    print(projects.count())
    users = User.objects.all()
    chat_form = MessageForm()
    context['target_users'] = users
    context['chat_form'] = chat_form
    if request.method == 'POST':
        f = MessageForm(request.POST)
        print('aaa')
        if f.is_valid():
            print('save')
            to_name = f.cleaned_data.get('mto')
            mto = User.objects.filter(username=to_name).first()
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()

    context['navbar'] = 'dashboard'

    ##### ADDDDDing Chat here ##----------------------------------------------------------------------------------------------
    # if not request.user.is_authenticated:
    #     return redirect(reverse_lazy('login'))
    # context = {}
    if request.method == 'POST':
        f = MessageForm(request.POST)
        print('aaa')
        if f.is_valid():
            print('save')
            to_name = f.cleaned_data.get('mto')
            mto = User.objects.filter(username=to_name).first()
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()

    search_text = ''
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
    if search_text:
        search_text = search_text.strip()
    talks = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).order_by('-msgTime')
    if search_text:
        last_msgs = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).filter(msg__icontains=search_text).order_by('-msgTime')[:10]
    else:
        last_msgs = talks[:10]

    talkers = set()
    for talk in talks:
        if len(talkers) >= 5:
            break
        if talk.mto == request.user:
            talkers.add(talk.mfrom)
        else:
            talkers.add(talk.mto)
    
    last_talks = []
    for talker in talkers:
        last_talks.append([talker, Message.objects.filter(Q(mto=talker, mfrom=request.user) | Q(mto=request.user, mfrom=talker)).order_by('-msgTime')[:10]])
    form = MessageForm()
    context['last_msgs'] = last_msgs
    context['chat_form'] = form
    context['last_talks'] = last_talks
    context['target_users'] = User.objects.all()

    context['navbar'] = 'chat'
    #####----------------------------------------------------------------------------------------------
    ##### ADDDDDing Contacts here ##-----------------------------------------------------------------------
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
    return render(request, 'dashboard/dashboard.html', context)

def projectView(request, project_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    project = Project.objects.filter(id=project_id).first()
    if project:
        res = model_to_dict(project, fields=['id', 'name', 'deadline', 'description', 'tasks'])
        file_query = ProjFile.objects.filter(project=project)
        file_number = file_query.count()
        file_infos = [str(f.filename) for f in file_query]
        tasks = Task.objects.filter(project=project).all()
        res['task_texts'] = [t.name for t in tasks]
        if len(tasks):
            res['ratio'] = round(len([t.name for t in tasks if t.status]) / len(tasks) * 100)
        else:
            res['ratio'] = 0
        res['file_number'] = file_number
        res['file_infos'] = file_infos
        res['create_user'] = project.create_user.username
        return JsonResponse(res)
