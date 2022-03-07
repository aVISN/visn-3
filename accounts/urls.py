from django.urls import path
from . import views
# from .views import CustomLoginView

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('pass_change/', views.passwordChange, name='pass_change'),
    path('email_change/', views.changeEmail, name='email_change'),
]