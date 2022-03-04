#!/usr/bin/env python
# coding: utf-8

# # Dialogflow API
# * Dialogflow = 구글에서 개발한 챗봇 개발 플랫폼
# * https://dialogflow.cloud.google.com/
# 
# 
# * 프로젝트 ID = newagent-ocwf
# * 언어 코드 = ko
# * 세션 ID = 세션 식별 용도로, 스트링 랜덤하게 가능
# * json 키 파일은 구글 클라우드 플랫폼에서 얻을 수 있음

# In[ ]:


from lms_crawl import Lms_crawl

import time
import random
from selenium import webdriver
import requests
from tabulate import tabulate


import os
from google.cloud import dialogflow

# 오류나면 다운로드)
# pip install google-cloud-dialogflow


# google cloud platform - IAM 및 관리자
# https://console.cloud.google.com/iam-admin/iam?project=newagent-ocwf
# 서비스 계정 생성 후 IAM에 추가를 해야 오류가 안남!!
# json 형식의 key는 google cloud platform - IAM 및 관리자 - 서비스 계정 - 키
# 에서 얻을 수 있음!!!!
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

# 프로젝트 아이디 - diaglogflow 설정 general에서 확인
DIALOGFLOW_PROJECT_ID = 'newagent-ocwf'
# 언어 - diaglogflow 설정 languages에서 확인
DIALOGFLOW_LANGUAGE_CODE = 'ko'
# 같은 세션인지 확인하는 용도, 아무 스트링이면 ok
SESSION_ID = 'mm'
# 챗봇 돌릴 텍스트
# TEXTS = ["알고리즘 이번 과제 몇점이야?", "지능정보시스템 강의 출석 현황 알려줘", "컴퓨터네트워크 출석 알려줘", "제출한 강의 알려줘", "안녕", "폴백 유도 텍스트"]


# In[ ]:


def detect_intent_texts(crawler, project_id, session_id, texts, language_code, year, semester, names):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        print("=" * 20)
        print()
        print("질의 : {}".format(response.query_result.query_text))
        print(
            "식별한 인텐트: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        
        # 챗봇의 답장
        ftext = response.query_result.fulfillment_text
        
        # 강의 이름이 text에 있다면 변수에 저장
        for name in names:
            if name in text:
                course_name = name
        
        
        if ftext == "강의":
            print("답장 :", ftext)
            table = crawler.course_check(course_name, year, semester)
            crawler.not_checked(table)
            result = ""
            result += '<'+ course_name +'><br>'
            result += crawler.print_table(table, 'c')
            print(result)
            return result
            
        elif ftext == "과제":
            print("답장 :", ftext)
            table = crawler.assign_check(course_name, year, semester)
            result = ""
            result += '<' + course_name + '><br>'
            result += crawler.print_table(table, 'a')
            print(result)
            return result
                
        elif ftext == "성적":
            print("답장 :", ftext)
            table = crawler.grade_check(course_name, year, semester)
            result = ""
            result += '<' + course_name + '><br>'
            result += crawler.print_table(table, 'g')
            print(result)
            return result
            
        else:
            print("답장 :", ftext)
            return ftext
        print()


# In[ ]:

'''
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
d = webdriver.Chrome(options=options)

c = Lms_crawl(d)

user = input('ID : ')
pw = input('PW : ')

c.login(user, pw)

year = input('연도 : ')
semester= input('학기 : ')

names = c.find_course(year, semester)
print(names)
print()


# In[ ]:


# 실행
detect_intent_texts(c, DIALOGFLOW_PROJECT_ID, SESSION_ID, TEXTS, DIALOGFLOW_LANGUAGE_CODE)


# In[ ]:
'''