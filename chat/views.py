from django.shortcuts import render, redirect
from .models import *
from dashboard.forms import *
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict


# ------------------------ working Chat as a page -------------------------------------------
# def chatView(request):
#     if not request.user.is_authenticated:
#         return redirect(reverse_lazy('login'))
#     context = {}
#     if request.method == 'POST':
#         f = MessageForm(request.POST)
#         print('aaa')
#         if f.is_valid():
#             print('save')
#             to_name = f.cleaned_data.get('mto')
#             mto = User.objects.filter(username=to_name).first()
#             Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()

#     search_text = ''
#     if request.method == 'GET':
#         search_text = request.GET.get('search_text')
#     if search_text:
#         search_text = search_text.strip()
#     talks = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).order_by('-msgTime')
#     if search_text:
#         last_msgs = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).filter(msg__icontains=search_text).order_by('-msgTime')[:10]
#     else:
#         last_msgs = talks[:10]

#     talkers = set()
#     for talk in talks:
#         if len(talkers) >= 5:
#             break
#         if talk.mto == request.user:
#             talkers.add(talk.mfrom)
#         else:
#             talkers.add(talk.mto)
    
#     last_talks = []
#     for talker in talkers:
#         last_talks.append([talker, Message.objects.filter(Q(mto=talker, mfrom=request.user) | Q(mto=request.user, mfrom=talker)).order_by('-msgTime')[:10]])
#     form = MessageForm()
#     context['last_msgs'] = last_msgs
#     context['chat_form'] = form
#     context['last_talks'] = last_talks
#     context['target_users'] = User.objects.all()

#     context['navbar'] = 'chat'

#     return render(request, 'chat/chat.html', context)

# --------------Project view for json reference--------------------------------------
# def projectView(request, project_id):
#     if not request.user.is_authenticated:
#         return redirect(reverse_lazy('login'))
#     project = Project.objects.filter(id=project_id).first()
#     if project:
#         res = model_to_dict(project, fields=['id', 'name', 'deadline', 'description', 'tasks'])
#         file_query = ProjFile.objects.filter(project=project)
#         file_number = file_query.count()
#         file_infos = [str(f.filename) for f in file_query]
#         tasks = Task.objects.filter(project=project).all()
#         res['task_texts'] = [t.name for t in tasks]
#         if len(tasks):
#             res['ratio'] = round(len([t.name for t in tasks if t.status]) / len(tasks) * 100)
#         else:
#             res['ratio'] = 0
#         res['file_number'] = file_number
#         res['file_infos'] = file_infos
#         res['create_user'] = project.create_user.username
#         return JsonResponse(res)

# ----------------- new chat !!!(connect messages like page chat with contact_id for mto!! -----------------------------------
def chatView(request, contact_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('login'))
    mto = User.objects.filter(id=contact_id).first()
    
    if mto:
        res = model_to_dict(mto, fields=['id','username'])
        # return JsonResponse(res)
    # ####
    # context = {}

    print('mto:',mto)
    # print('request.method:',request.method)
    if request.method == 'POST':
        f = MessageForm(request.POST)
        # print('message:',Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto))
        print('form:',f)
        if f.is_valid():
            # print('save')
            to_name = mto #f.cleaned_data.get('mto')
            # mto = User.objects.filter(id=contact_id).first()
            
            Message(mfrom=request.user, msg=f.cleaned_data.get('message'), mto=mto).save()
            print('Message',Message)

    search_text = ''
    # if request.method == 'GET':
    #     search_text = request.GET.get('search_text')
    # if search_text:
    #     search_text = search_text.strip()
    talks = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).order_by('-msgTime')
    if search_text:
        last_msgs = Message.objects.filter(Q(mto=request.user) | Q(mfrom=request.user)).order_by('-msgTime')[:10]
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
    # for talker in talkers:
    #     last_talks.append([talker, Message.objects.filter(Q(mto=talker, mfrom=request.user) | Q(mto=request.user, mfrom=talker)).order_by('-msgTime')[:10]])

    talker = mto
    last_talks = [Message.objects.filter(Q(mto=talker, mfrom=request.user) | Q(mto=request.user, mfrom=talker)).order_by('-msgTime')[:10]]
    # form = MessageForm()
    # print(len(last_talks[0]))
    if(len(last_talks[0]) > 0):
        res['last_msgs'] =[model_to_dict(m, fields=['id','mfrom','mto','msg','msgTime']) for m in last_talks[0]]
        for m in last_talks[0]:
            # for msg in m:
            print('lastTalks:',m.msg)
    # print(last_talks[0][1][0].msg)
    # context['last_msgs'] = last_msgs
    # context['chat_form'] = form
    # context['last_talks'] = last_talks
    # context['target_users'] = User.objects.all()

    # context['navbar'] = 'chat'
    # print("last_talks:",last_talks[0],"-",last_talks[0][1][0].msg)
    # print("last_msgs:",last_msgs[0].msg)
    # if(last_talks[0])
    # ########
    # res['last_msgs'] = [model_to_dict(m, fields=['id','mfrom','mto','msg','msgTime']) for m in last_msgs] ##
    ########## res['last_msgs'] = model_to_dict(fields=['id','mfrom','mto','msg','msgTime']) ##
    # res['chat_form'] = form
    
    chatMessages = {}
    # for q in last_talks[0][1]:
    #     # print(q)
    #       chatMessages.append(q)
    # res['last_talks'] = model_to_dict(last_talks[0][1], fields=['id','mfrom','mto','msg','msgTime'])
    # res['last_talks'] = model_to_dict(last_talks, fields=['talker','Queryset'])#last_talks[0][1][m.msg for m in last_talks]#
    # res['target_users'] = User.objects.all()# res['task_texts'] = [t.name for t in tasks]

    # res['navbar'] = 'chat'
    return JsonResponse(res)
    # return render(request, 'chat/chat.html', context)
