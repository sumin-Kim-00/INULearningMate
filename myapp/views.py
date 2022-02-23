from django.shortcuts import render, HttpResponse
from django.contrib import messages

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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

# 프로젝트 아이디 - diaglogflow 설정 general에서 확인
DIALOGFLOW_PROJECT_ID = 'newagent-ocwf'
# 언어 - diaglogflow 설정 languages에서 확인
DIALOGFLOW_LANGUAGE_CODE = 'ko'
# 같은 세션인지 확인하는 용도, 아무 스트링이면 ok
SESSION_ID = 'mm'


# 이렇게 하면 클라이언트 하나만 접속 가능해서 조치 취해야 함..
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
d = webdriver.Chrome(options=options)

c = Lms_crawl(d)

year = '2021'
semester = '2'


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

    user = username
    pw = password

    c.login(user, pw)

    # 로그인 성공
    if d.current_url == 'https://cyber.inu.ac.kr/':

        names = c.find_course(year, semester)
        print(names)
        print()
        return render(request, 'chathome.html', context)

    # 로그인 실패시 알림 띄우고 다시 로그인 창으로 돌아감
    else:
        messages.info(request, "아이디와 비밀번호를 확인해주세요!")
        return render(request, 'login.html', context)


def chat(request):
    context = {}
    chat = []
    chatinput = request.POST['chatinput']
    chat.append(chatinput)

    print(chat)

    names = c.find_course(year, semester)
    print(names)

    chatbot.detect_intent_texts(c, DIALOGFLOW_PROJECT_ID, SESSION_ID, chat, DIALOGFLOW_LANGUAGE_CODE, year, semester, names)

    return render(request, 'chathome.html', context)

"""
def index(request):
    return HttpResponse('<h1>Random</h1>' + str(random.random()))  # Http를 이용해서 응답

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read!' + id )
"""