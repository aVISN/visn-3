from django.urls import path
from . import views
# from .views import CustomLoginView

urlpatterns = [
    path('', views.filesView, name='files'),
    path('new_file/', views.newFile, name='new_file'),
    path('del_file/<int:file_id>/', views.del_file, name='del_file'),
    path('<path:filepath>/', views.file_response_download1, name='download'),
]