#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import random
from selenium import webdriver
import requests
from tabulate import tabulate




class Lms_crawl:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://cyber.inu.ac.kr/login.php")

        
    def login(self, user, pw):
        self.driver.find_element('xpath', '//*[@id="input-username"]').send_keys(user)
        self.driver.find_element('xpath', '//*[@id="input-password"]').send_keys(pw)
        self.driver.find_element('xpath', '//*[@id="region-main"]/div/div/div/div[1]/div[1]/div[2]/form/div[2]/input').submit()
        
        
    def find_course_name(self):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        hrefs=self.driver.find_elements_by_css_selector(".course_link")

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
        return course_name
    
    def find_course_name_id(self):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        hrefs=self.driver.find_elements_by_css_selector(".course_link")
        
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
        course_name_id=dict(zip(course_name,course_number))
        
        return course_name_id
    
    
    def print_table(self, table, ttype):
        if ttype == 'c':
            return(tabulate(table, headers=["주", "강의 자료", "총 학습 시간", "열람 횟수", "출석", "주차 출석"], tablefmt="html"))
        elif ttype == 'a':
            return(tabulate(table, headers=["주", "과제", "종료 일시", "제출", "성적"], tablefmt="html"))
        elif ttype == 'g':
            return(tabulate(table, headers=["성적 항목", "성적", "석차", "평균", "피드백"], tablefmt="html"))
        else:
            return('잘못된 형식입니다.')
        
    
    def not_checked(self, table):
        find = False

        for t in table:
            if t[-1] == 'X':
                print(t[0] +'주차의 \'' + t[1] + '\' 영상을 아직 학습하지 않았습니다.')
                find = True

        if not find:
            print('모든 강의를 학습하셨습니다.')
            
            
    
    def course_check(self, name , course_name_id):
        # main
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        find = False
        hrefs=self.driver.find_elements_by_css_selector(".course_link") #접근
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
                    progress_url="https://cyber.inu.ac.kr/report/ubcompletion/user_progress_a.php?id="+str(course_name_id[name])
                    self.driver.get(progress_url)
                    # 강의 테이블 리스트 형태로 저장
                    table = []

                    tbody = self.driver.find_element('xpath', '//*[@id="ubcompletion-progress-wrapper"]/div[2]/table/tbody')
                    rows = tbody.find_elements_by_tag_name("tr")
                    # 값 추가
                    for row in rows:
                        trtable = []
                        tds = row.find_elements_by_tag_name("td")

                        for td in tds:
                            tdtable = []
                            tdtext = td.text.split("\n")
                            tdtable.append(tdtext)                 
                            tdtable = sum(tdtable, [])
                            trtable.append(tdtable)
                        trtable = sum(trtable, [])          
                        table.append(trtable)

                    # 값 정리
                    i = 0
                    for t in table:
                        row = t
                        if row[-2] == 'O' or row[-2] == 'X' or row[-2] == ' ':
                            pass
                        else:
                            row.insert(0, ' ')
                            row.append(' ')  

                        if row[-2] == ' ':
                            row.append(' ') 

                        del row[2]
                        table[i] == row
                        i += 1

                    return table
                except:
                    alert= self.driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                    return alert.text
                
        else:
            t = ['강의를 찾지 못했습니다.']
            return t
            

        
        
    def assign_check(self,name,course_name_id):
        # main
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        find = False
        hrefs=self.driver.find_elements_by_css_selector(".course_link") #접근
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
                assign_url="https://cyber.inu.ac.kr/mod/assign/index.php?id="+str(course_name_id[name])
                self.driver.get(assign_url)
                tbody = self.driver.find_element('xpath', '//*[@id="region-main"]/div/table/tbody')
                rows = tbody.find_elements_by_tag_name("tr")
                table = []

                for row in rows:
                    trtable = []
                    tds = row.find_elements_by_tag_name("td")        
                    for td in tds:
                        tdtable = []
                        tdtext = td.text.split("\n")
                        tdtable.append(tdtext)                 
                        tdtable = sum(tdtable, [])
                        trtable.append(tdtable)
                    trtable = sum(trtable, [])          
                    table.append(trtable)
                return table
            except:
                alert= self.driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                return alert.text
                
        else:
            t = ['강의를 찾지 못했습니다.']
            return t
        
    def grade_check(self, name,course_name_number):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        find = False
        hrefs=self.driver.find_elements_by_css_selector(".course_link") #접근
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
                    progress_url="https://cyber.inu.ac.kr/grade/report/user/index.php?id="+str(course_name_number[name])
                    self.driver.get(progress_url)
                    tbody = self.driver.find_element('xpath', '//*[@id="region-main"]/div/table/tbody')
                    rows = tbody.find_elements_by_tag_name("tr")

                    table = []

                    for row in rows:
                        trtable = []
                        spans = row.find_elements_by_tag_name("span")
                        if len(spans) != 0:
                            for span in spans:
                                trtable.append(span.text.split("\n"))

                        #과제명은 태그 a에 있음
                        tag_a = row.find_elements_by_tag_name("a")  
                        for a in tag_a:
                            trtable.append(a.text.split("\n"))

                        tds = row.find_elements_by_tag_name("td")
                        i = 1
                        for td in tds:
                            tdtable = []
                            tdtext = td.text.split("\n")

                            print_seq = [2, 6, 7, 8]  # 성적항목, 성적, 석차, 평균, 피드백만을 가져오기 위해
                            if i in print_seq:
                                tdtable.append(tdtext)
                            i += 1

                            tdtable = sum(tdtable, [])
                            trtable.append(tdtable)

                        trtable = sum(trtable, [])
                        table.append(trtable)
                    table.pop(0)
                    return table
                except:
                    t = ['영상 정보가 없거나 잘못되었습니다.']
                    return t
        else:
            t = ['강의를 찾지 못했습니다.']
            return t

        #이번주 강의 주차 찾기
    def thisweek(self, name,course_name_id):
        # main
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        find = False
        hrefs=self.driver.find_elements_by_css_selector(".course_link") #접근
        full_course_name=[]
        course_name=[]
        tmp=[]
        for i in hrefs:
            full_course_name.append(i.text)
        for i in range(len(full_course_name)):
            tmp.append(full_course_name[i].split("\n"))
            course_name.append(tmp[i][1])
            if("NEW" in course_name[i]):
                course_name[i]=course_name[i][:-3]
            course_name[i]=course_name[i][:-19]      
        if name in course_name:
            find = True  
            if find:
                    course_url="https://cyber.inu.ac.kr/course/view.php?id="+str(course_name_id[name])
                    self.driver.get(course_url)
                    element= self.driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                    list=element.text.split("\n")
                    if len(list)>3: return list[7][0]
                    else: return list[:-1]
        else:
            t = ['강의를 찾지 못했습니다.']
            return t
    #thisweek에 해당하는 테이블 출력(일단 출석기준으로만 해봄)
    def thisweek_course(self, coursetable, thisweek):
        thisweek_list=[]
        for i in range(len(coursetable)):
            if coursetable[i][0] in thisweek[0]:
                while (coursetable[i][0]==' ')or(coursetable[i][0]==thisweek[0]):                
                        thisweek_list.append(coursetable[i])
                        i+=1
        if len(thisweek_list)==0:
            thisweek_list.append("해당주차가 없습니다")
        return thisweek_list
    
    #미완성
    def notice(self,name,course_name_number):
        url = 'https://cyber.inu.ac.kr/'
        self.driver.get(url)
        find = False
        hrefs=self.driver.find_elements_by_css_selector(".course_link") #접근
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
                    self.driver.get(course_main)
                    self.driver.find_element('xpath', '//*[@id="page-container"]/div[1]/div/div/div/div[2]/div/a').click()
                    notice_list=self.driver.find_elements_by_css_selector(".list") #접근
                    
                    tmp=[]
                    notice=[]
                    notice_link=[]
                    for i in notice_list:
                        tmp.append(i.text)
                    for i in range(len(tmp)):
                        notice.append(tmp[i].split("\n"))
                    return notice[1]
                except:
                    alert= self.driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                    return alert.text[:-2]
                
        else:
            t = ['강의를 찾지 못했습니다.']
            return t
                