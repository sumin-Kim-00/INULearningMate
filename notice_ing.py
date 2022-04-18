#의문인 부분: a태그 부분 내용은 크롤링이 되는데 그거의 href는 none으로 없다고 나옴
#쥬피터에서 하던대로 올린거 

import random
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from tabulate import tabulate
import os
from webdriver_manager.chrome import ChromeDriverManager #pip install webdriver-manager

def login(idd, pw):
    driver.find_element_by_id('input-username').send_keys(idd)
    driver.find_element_by_id('input-password').send_keys(pw)
    driver.find_element_by_name('loginbutton').submit()

def find_course():
    # 수강 페이지로 이동
    url = 'https://cyber.inu.ac.kr/'
    driver.get(url)
    hrefs=driver.find_elements_by_css_selector(".course_link")
    
    course_number=[] 
    full_course_name=[]
    course_name=[]
    tmp=[]
    
    for i in hrefs:
        full_course_name.append(i.text)
        course_number.append(i.get_attribute('href'))
        
    #링크 중에 번호만 리스트 삽입
    for i in range(len(course_number)): 
        course_number[i]=course_number[i][-5:] 
        
    #이름 가공
    for i in range(len(full_course_name)):
        tmp.append(full_course_name[i].split("\n"))
        course_name.append(tmp[i][1])
        if("NEW" in course_name[i]):
            course_name[i]=course_name[i][:-3]
        course_name[i]=course_name[i][:-19]     
    
    
    #dict(name:id_number)
    course_name_number=dict(zip(course_name,course_number))
    

    return course_name_number

def click_notice(name,course_name_number):
    url = 'https://cyber.inu.ac.kr/'
    driver.get(url)
    find = False
    hrefs=driver.find_elements_by_css_selector(".course_link") #접근
    full_course_name=[]
    course_name=[]
    tmp=[]
    for i in hrefs:
        full_course_name.append(i.text)
    #이름 가공
    for i in range(len(full_course_name)):
        tmp.append(full_course_name[i].split("\n"))
        course_name.append(tmp[i][1])
        if("NEW" in course_name[i]):
            course_name[i]=course_name[i][:-3]
        course_name[i]=course_name[i][:-19]  

    if name in course_name:
        find = True        
        if find:
            try:
                course_main=('https://cyber.inu.ac.kr/course/view.php?id='+str(course_name_number[name]))
                driver.get(course_main)
                driver.find_element('xpath', '//*[@id="page-container"]/div[1]/div/div/div/div[2]/div/a').click()
                notice_link=[]
                notice_a=[]
                notice_td=driver.find_elements_by_tag_name("td")  

                #***********************************************************************************************
                for i in notice_td:
                    notice_a.append(i.find_elements_by_tag_name("a"))


                elems = driver.find_elements_by_xpath("//a[@href]")
                for elem in elems:
                    if "https://cyber.inu.ac.kr/mod/ubboard/article.php?id=" in elem.get_attribute("href"):
                        notice_link.append(elem.get_attribute("href"))


                #**********************************************************************************************

                return notice_link #notice_link=href 크롤링 
                # 의문인 부분: a태그 부분 내용은 크롤링이 되는데 그거의 href는 none으로 없다고 나옴
            except Exception as e:
                #alert= driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                #return alert.text[:-2]
                print(e)

    else:
        t = ['강의를 찾지 못했습니다.']
        return t

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://cyber.inu.ac.kr/")

idd=201901634
pw="aaaa1111!"
login(idd,pw)
names = find_course()
list=click_notice('공직사회의이해',names)
print(list)
