from django.shortcuts import render, redirect
from django.db.models import Q
from dashboard.forms import *
from .models import *
import math
from django.urls import reverse_lazy


def contactsView(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    context = {}
    last_msgs = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).order_by('-msgTime')[:12]
    # print(last_msgs)
    user_groups = []
    users = []
    for msg in last_msgs:
        if msg.mto == request.user:
            if msg.mfrom not in users:
                users.append(msg.mfrom)
        else:
            if msg.mto not in users:
                users.append(msg.mto)
    for user in users:
        print(user.username, user.first_name, user.last_name, user.email)
    for i in range(math.ceil(len(users)/3)):
        user_groups.append(users[i * 3: (i + 1) * 3])

    #----
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

    #---- 

    context['user_groups'] = user_groups
    if request.method == 'POST':
        f = MessageForm(request.POST)
        print('aaa')
        if f.is_valid():
            print('save')
            to_name = f.cleaned_data.get('mto')
            mto = User.objects.filter(username=to_name).first()
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()
    context['chat_form'] = MessageForm()
    context['target_users'] = User.objects.all()
    context['navbar'] = 'contacts'

    return render(request, 'contacts.html', context)
