from __future__ import division
import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import App_Session

# python files
import chatbot
from lms_crawl import Lms_crawl
import stt

# web crawling
import time
import random
from selenium import webdriver
import requests
from tabulate import tabulate

# chatbot
import os
from google.cloud import dialogflow

# speech to text
import re
import sys
from google.cloud import speech
import pyaudio
from six.moves import queue

from myapp.models import App_Session
from django.contrib.auth import authenticate, login


# 첫 번째 파라미터로 요청과 관련된 여러가지 정보가 들어있는 객체를 전달해주도록 되어있음(request)

# 프로젝트 아이디 - diaglogflow 설정 general에서 확인
DIALOGFLOW_PROJECT_ID = 'newagent-ocwf'
# 언어 - diaglogflow 설정 languages에서 확인
DIALOGFLOW_LANGUAGE_CODE = 'ko'
# 같은 세션인지 확인하는 용도, 아무 스트링이면 ok
SESSION_ID = 'mm'

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

options = webdriver.ChromeOptions()

prefs = {'profile.default_content_setting_values': {
    'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 
    'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 
    'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 
    'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 
    'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 
    'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 
    'site_engagement' : 2, 'durable_storage' : 2}} 
options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


def home(request):
    print(request.session.session_key)
    context = {}

    # 아이디, 비밀번호가 담긴 쿠키가 존재할 때 - 강의를 찾아 chathome.html으로 바로 반환함
    if request.COOKIES.get('username') is not None and request.COOKIES.get('password') is not None:
        request.session['username'] = request.COOKIES.get('username')
        request.session['password'] = request.COOKIES.get('password')
        user = request.session['username']
        pw = request.session['password']

        d = webdriver.Chrome(options=options)
        c = Lms_crawl(d)

        c.login(user, pw)

        names = c.find_course_name()
        print(names)
        print()

        context = {
            'username': user,
            'password': pw,
            'courses' : names
        }

        return render(request, "chathome.html", context)

    # 쿠키 존재 X
    request.session['username'] = 'user'
    request.session['password'] = 'pw'

    return render(request, "login.html", context)


def login(request):
    d = webdriver.Chrome(options=options)

    c = Lms_crawl(d)

    username = request.POST['username']
    password = request.POST['password']

    request.session['username'] = username
    request.session['password'] = password

    user = request.session['username']
    pw = request.session['password']

    context = {
        'username': user,
        'password': pw
    }

    c.login(user, pw)

    # 로그인 성공
    if d.current_url == 'https://cyber.inu.ac.kr/':
        # 자동 로그인 체크 시
        if request.POST.getlist('autologin'):
            autologin = True
            print("autologin =", autologin)

            names = c.find_course_name()
            print(names)
            print()
            context['courses'] = names

            # request.session.set_expiry(2592000)
            expire = datetime.datetime.now() + datetime.timedelta(days = 30)
            
            response = render(request, 'chathome.html', context) 
            response.set_cookie('username', username, expires=expire)
            response.set_cookie('password', password, expires=expire)

            return response

        # 자동 로그인 체크 X
        autologin = False

        print("autologin =", autologin)

        names = c.find_course_name()
        print(names)
        print()
        context['courses'] = names

        return render(request, 'chathome.html', context)

    # 로그인 실패시 알림 띄우고 다시 로그인 창으로 돌아감
    else:
        messages.info(request, "아이디와 비밀번호를 확인해주세요!")
        return render(request, 'login.html', context)


def chat(request):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'chatkey.json'

    d = webdriver.Chrome(options=options)

    c = Lms_crawl(d)

    user = request.session['username']
    pw = request.session['password']

    c.login(user, pw)

    chat = []
    chatinput = request.GET['chatinput']
    chat.append(chatinput)

    print(chat)

    names = c.find_course_name()
    print(names)
    course_name_id=c.find_course_name_id()
    
    chat = chatbot.detect_intent_texts(c, DIALOGFLOW_PROJECT_ID, SESSION_ID, chat, DIALOGFLOW_LANGUAGE_CODE, names, course_name_id)
    

    chatanswer = chat
    # print(chatanswer)

    context = {
        'username': user,
        'password': pw,
        'chatanswer': chatanswer,
        'courses': names,
        'flag': '0'
    }

    return JsonResponse(context, content_type="application/json")


def speechtottext(request):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'sttkey.json'
    chat = stt.run()
    
    speechtext = chat
    # print(chatanswer)

    context = {
        'speechtext': speechtext,
        'flag': '0'
    }
    return JsonResponse(context, content_type="application/json")


def logout(request):
    context = {}
    response = render(request, 'login.html', context)
    if request.COOKIES.get('username') is not None and request.COOKIES.get('password') is not None:
        response.delete_cookie('username')
        response.delete_cookie('password')

    return response

"""
def index.html(request):
    return HttpResponse('<h1>Random</h1>' + str(random.random()))  # Http를 이용해서 응답

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read!' + id )
"""