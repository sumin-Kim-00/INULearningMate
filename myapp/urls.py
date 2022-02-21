from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.home),
    path('result', views.result, name='result'),
    path('login', views.login, name='login'),
    path('chat', views.chat, name='chat'),
    #path('create/', views.create),
    #path('read/<id>/', views.read)
]
