from django.shortcuts import render, HttpResponse
import chatbot
from lms_crawl import Lms_crawl
import time
import random
from selenium import webdriver
import requests
from tabulate import tabulate


import os
from google.cloud import dialogflow
# 첫 번째 파라미터로 요청과 관련된 여러가지 정보가 들어있는 객체를 전달해주도록 되어있음(request)

def home(request):
    context = {}

    return render(request, "login.html", context)

def result(request):
    name = request.POST['username']
    students = ['amy', 'bob', 'catherine', 'dennis', 'ethan']

    if name in students:
        is_exist = True
    else:
        is_exist = False

    return render(request, 'test.html', {'user_name': name, 'is_exist': is_exist})

def login(request):
    context = {}

    username = request.POST['username']
    password = request.POST['password']

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    d = webdriver.Chrome(options=options)

    c = Lms_crawl(d)

    user = username
    pw = password

    c.login(user, pw)

    #year = input('연도 : ')
    #semester = input('학기 : ')

    year = '2021'
    semester = '2'

    names = c.find_course(year, semester)
    print(names)
    print()
    return render(request, 'chathome.html', context)


"""
def index(request):
    return HttpResponse('<h1>Random</h1>' + str(random.random()))  # Http를 이용해서 응답

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read!' + id )
"""