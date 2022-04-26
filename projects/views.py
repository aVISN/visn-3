from asyncio import tasks
from unittest import result
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
import math
from dashboard.forms import *
from .models import *

def projectsView(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    context = {}
    print(Project.objects.all().count())
    search_text = request.GET.get('search_text')
    if search_text:
        search_text = search_text.strip()
        projects = Project.objects.filter(create_user=request.user).filter(name__contains=search_text).all()
        projects2 = request.user.pmembers.filter(name__contains=search_text).all()
    else:
        projects = Project.objects.filter(create_user=request.user).all()
        projects2 = request.user.pmembers.all()
    projects = list(projects)
    for p in projects2:
        if p not in projects:
            projects.append(p)
    results = []
    for i in range(math.ceil(len(projects)/3)):
        results.append(projects[i *3: (i+1)*3])
    
    context['projects'] = results
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

    context['navbar'] = 'projects'
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

    return render(request, 'projects/projects.html', context)

def singleProjectView(request, project_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    context = {}
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return redirect(reverse_lazy('projects'))
    context['project'] = project
    context['files'] = ProjFile.objects.filter(project=project).all()
    users = User.objects.all()

    proj_members = list(project.members.all())
    proj_non_members = set(users) - set(proj_members)
    if project.create_user in proj_members:
        proj_members.remove(project.create_user)
    if project.create_user in proj_non_members:
        proj_non_members.remove(project.create_user)
    
    context['proj_members'] = proj_members
    context['proj_non_members'] = proj_non_members

    chat_form = MessageForm()
    context['target_users'] = users
    context['chat_form'] = chat_form
    if request.method == 'POST':
        f = MessageForm(request.POST)
        if f.is_valid():
            to_name = f.cleaned_data.get('mto')
            mto = User.objects.filter(username=to_name).first()
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()

    return render(request, 'projects/project.html', context)


def createProjectView(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    context = {}
    freelancer = User.objects.filter(is_superuser = True)
    print(freelancer)
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

    form = NewProjForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        if Project.objects.filter(name=form.cleaned_data.get('name')):
            return redirect(reverse_lazy('projects'))
        p = Project(create_user=request.user, deadline=form.cleaned_data.get('deadline'),
            description=form.cleaned_data.get('description'), name=form.cleaned_data.get('name'),
            tasks=form.cleaned_data.get('tasks'))

        
        p.save()
        print("formdata: ",form.cleaned_data.get('members'))
        for m in form.cleaned_data.get('members')[:]:
            if (m != request.user):
                p.members.add(request.user)
            print(m)
            p.members.add(m)
        # adds freelancer to project
        p.members.add(freelancer[0])
        
        p.save()
        # name = form.cleaned_data.get('name')
        return redirect(reverse_lazy('projects'))  #
    else:
        form = NewProjForm()
        context['form'] = form
        return render(request, 'projects/new_project.html', context)

def addTask(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            Task(name=form.cleaned_data.get('name'), project=form.cleaned_data.get('project')).save()
            
    form = NewTaskForm()
    form.fields['project'].queryset  = Project.objects.filter(create_user=request.user).all()
    return render(request, 'projects/new_task.html', {'form': form})

def addMember(request, project_id, user_id):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return JsonResponse({'status': 0, 'info': 'Project was not existed!'})
    user = User.objects.filter(id=user_id).first()
    if not project:
        return JsonResponse({'status': 0, 'info': 'User was not existed!'})
    project.members.add(user)
    project.save()
    return JsonResponse({'status': 1, 'info': 'success!'})

def delMember(request, project_id, user_id):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return JsonResponse({'status': 0, 'info': 'Project was not existed!'})
    user = User.objects.filter(id=user_id).first()
    if not project:
        return JsonResponse({'status': 0, 'info': 'User was not existed!'})
    project.members.remove(user)
    project.save()
    return JsonResponse({'status': 1, 'info': 'success!'})
