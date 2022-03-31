# INULearningMate
        if "공지" in ftext:
            if in_names:
                print("답장 :", ftext)
                result = crawler.notice(course_name,course_name_id)
                result = ""
                result += '<' + course_name + '><br><br>'
                print(result)
                return result
            else:
                result="어떤 과목의 성적을 알고 싶으세요?<br>"
                result += '<div class="cnBtn">'
                for i in range(len(names)):
                   result += '<div><button onclick="cn_btn_notice()" value="'+ names[i] + '">'+ names[i]+'</button></div>'
                result += '</div>'
                return result
        else:
            print("답장 :", ftext)
            return ftext