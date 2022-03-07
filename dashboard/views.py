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
    projects = Project.objects.filter(Q(create_user=request.user) | Q(members=request.user)).all()[:]
    res = []
    for i in range(math.ceil(len(projects)/3)):
        res.append(projects[i * 3: (i+1)*3])
    context['projects'] = res
    print(projects)
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
    return render(request, 'dashboard/dashboard.html', context)

def projectView(request, project_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    project = Project.objects.filter(id=project_id).first()
    if project:
        res = model_to_dict(project, fields=['id', 'name', 'deadline', 'discription', 'tasks'])
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
