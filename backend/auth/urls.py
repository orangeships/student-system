from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='auth_register'),
    path('login/', views.login, name='auth_login'),
    path('user/', views.user_profile, name='auth_user_profile'),
    path('profile/', views.update_profile, name='auth_update_profile'),
]