from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('', views.home)
    #path('create/', views.create),
    #path('read/<id>/', views.read)
]
