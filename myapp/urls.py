from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.home),
    path('login', views.login, name='login'),
    path('chat', views.chat, name='chat'),
    path('speechtottext', views.speechtottext, name='speechtottext'),
    path('logout', views.logout, name='logout'),
]
