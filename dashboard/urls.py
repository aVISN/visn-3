from unicodedata import name
from django.urls import include,path
from . import views
# from .views import CustomLoginView

from chat.views import chatView
from contacts.views import contactsView

urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='login'),
    path('', views.dashboardView, name='dashboard'),
    path('project_view/<int:project_id>/', views.projectView, name='project_view'),
    # path('contact_view/', contactsView, name='project_view'), #--- chat contacts ---
    path('chat_view/<int:contact_id>/', chatView, name='chat_view'), #----- chat ----
    # path('chat/', include('chat.urls', namespace='chat')),
]