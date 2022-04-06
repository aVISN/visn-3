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
    # last_msgs = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).order_by('-msgTime')[:12]
    # print(last_msgs)
    user_groups = []
    users = []
    # for msg in last_msgs:
    #     if msg.mto == request.user:
    #         if msg.mfrom not in users:
    #             users.append(msg.mfrom)
    #     else:
    #         if msg.mto not in users:
    #             users.append(msg.mto)
    # for user in users:
    #     print(user.username, user.first_name, user.last_name, user.email)
    # for i in range(math.ceil(len(users)/3)):
    #     user_groups.append(users[i * 3: (i + 1) * 3])

    #----
    # memberPIDs = []
    contacts = []
    projects = Project.objects.all()
    for project in projects:
        print("project: ",project)
        members = project.members.all()
        foundMatch = False
        for member in members:
            print("member: ",member)
            if(member == request.user):
                # memberPIDs.append(project.pk)
                foundMatch = True
                # print("!",project.pk,",",members,"!")
        if(foundMatch):
            for member in members:
                if(member != request.user):
                    contacts.append(member)
                    print("@",member)

    context['contacts'] = contacts

    # for p_id in memberPIDs:
    #     for member in projects.p_id.members:
    #         if(member != request.user):
    #             user_group.append(member)

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
