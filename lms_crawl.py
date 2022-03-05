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
        
        
    def find_course(self, year, semester):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/local/ubion/user/?year=' + year + '&semester=' + semester + '0'
        self.driver.get(url)

        # 강의 이름 찾아서 리스트에 추가
        name = []
        for i in range(1,15):
            try:
                course_url = self.driver.find_element('xpath', '//*[@id="region-main"]/div/div/div[2]/div/table/tbody/tr[' + str(i) + ']/td[3]/div/a')
                course_name = course_url.text[:-13]
                name.append(course_name)
            except:
                break

        return name
    
    
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
            
            
    
    def course_check(self, name, year, semester):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/local/ubion/user/?year=' + year + '&semester=' + semester + '0'
        self.driver.get(url)

        # 강의를 찾았는지 여부 확인
        find = False

        for i in range(1,15):
            try:
                course_url = self.driver.find_element('xpath', '//*[@id="region-main"]/div/div/div[2]/div/table/tbody/tr[' + str(i) + ']/td[3]/div/a')
                course_name = course_url.text[:-13]
                if course_name == name:
                    find = True
                    break
            except:
                pass

        # 강의를 찾으면:
        if find:
            try:
                course_url.click()
                # 온라인 출석부
                self.driver.find_element('xpath', '//*[@id="coursemos-course-menu"]/ul/li[1]/div/div[2]/ul/li[2]/ul/li[1]/a').click()

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
                t = ['영상 정보가 없거나 잘못되었습니다.']
                return t
        else:
            t = ['강의를 찾지 못했습니다.']
            return t

        
        
    def assign_check(self, name, year, semester):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/local/ubion/user/?year=' + year + '&semester=' + semester + '0'
        self.driver.get(url)

        # 강의를 찾았는지 여부 확인
        find = False

        for i in range(1,15):
            try:
                course_url = self.driver.find_element('xpath', '//*[@id="region-main"]/div/div/div[2]/div/table/tbody/tr[' + str(i) + ']/td[3]/div/a')
                course_name = course_url.text[:-13]
                if course_name == name:
                    find = True
                    break
            except:
                pass

        # 강의를 찾으면:
        if find:
            try:
                course_url.click()
                # 과제
                self.driver.find_element('xpath', '//*[@id="coursemos-course-menu"]/ul/li[2]/div/div[2]/ul/li[3]/a').click()
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
                t = ['영상 정보가 없거나 잘못되었습니다.']
                return t
        else:
            t = ['강의를 찾지 못했습니다.']
            return t
        
        
    def grade_check(self, name, year, semester):
        # 수강 페이지로 이동
        url = 'https://cyber.inu.ac.kr/local/ubion/user/?year=' + year + '&semester=' + semester + '0'
        self.driver.get(url)

        try:
            for i in range(1, 15):
                try:
                    course_url = self.driver.find_element('xpath', '//*[@id="region-main"]/div/div/div[2]/div/table/tbody/tr[' + str(i) + ']/td[3]/div/a')
                    course_name = course_url.text[:-13]
                    if course_name == name:
                        break
                except:
                    pass

            course_url.click()

            # 성적부 Xpath
            self.driver.find_element('xpath', '//*[@id="coursemos-course-menu"]/ul/li[1]/div/div[2]/ul/li[2]/ul/li[3]/a').click()

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
            return 0
