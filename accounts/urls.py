from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    url('', include('social_django.urls', namespace='social')),
    path('dashboard', views.dashboard, name='dashboard')
]
