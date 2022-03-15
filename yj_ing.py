#이번주 강의 주차 찾기
def this_week(name,course_name_id):
    # main
    url = 'https://cyber.inu.ac.kr/'
    driver.get(url)
    find = False
    hrefs=driver.find_elements_by_css_selector(".course_link") #접근
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
                course_url="https://cyber.inu.ac.kr/course/view.php?id="+str(course_name_number[name])
                driver.get(course_url)
                element= driver.find_element('xpath', '//*[@id="region-main"]/div/div[1]')
                list=element.text.split("\n")
                if len(list)>3: return list[7]
                else: return list[:-1]
    else:
        t = ['강의를 찾지 못했습니다.']
        return t

#thisweek에 해당하는 테이블 출력(일단 출석기준으로만 해봄)
def thisweek_course(course, thisweek):
    thisweek_list=[]
    for i in range(len(course)):
        if course[i][0]==thisweek[0]:
            while (course[i][0]==' ')or(course[i][0]==thisweek[0]):                
                    thisweek_list.append(course[i])
                    i+=1
    if len(ii)==0:
        thisweek_list.append("해당주차가 없습니다")
    return thisweek_list

