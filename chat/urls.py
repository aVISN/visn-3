from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views
# from .views import CustomLoginView

app_name='chat'

urlpatterns = [
    path('', views.chatView, name='chat'), 
]