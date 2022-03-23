#미완성
'''
문제1) 강의 id가 공지에서는 바뀜, xpath도 과목마다 번호가 다름
문제2) 그래도 크롤링은 되는데 너무 많은것들이 긁어져서 어떻게 걸러야할지 잘 모르겠음 
'''
def notice(self,name,course_name_number):
    url = 'https://cyber.inu.ac.kr/'
    self.driver.get(url)
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
                self.driver.get(course_main)
                self.driver.find_element('xpath', '//*[@id="module-760225"]/div/div/div[2]/div/a').click()
                for i in range(1,10):
                    try:
                        notice_list = self.driver.find_element('xpath', '//*[@id="ubboard_list_form"]/table/tbody/tr[',str(i),']/td[2]/a')
                        notices=notice_list.text
                    except:
                        pass
                return notices

            except:
                alert= self.driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                return alert.text
            
    else:
        t = ['강의를 찾지 못했습니다.']
        return t
            