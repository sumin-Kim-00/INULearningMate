# INULearningMate

### 2022.02.21)<br>
------------
###### 다영 )
* form 태그 사용해서 post 방식 request 처리 연습하기 위해 test.html 추가하고, urls, views 수정함 <br>
* 채팅용으로 html 하나만 써야할 것 같은데 이 방식 어떻게 활용해보면 될듯..?<br>
* 그리고 실제로 구현할 때 chatbot.py나 lms_crawl.py는 view 부분에 직접적으로 넣거나 호출해야할 것 같아<br>

--------------
###### 다영 )
* lms 로그인 간단하게 구현했어 
* login.html에 로그인 페이지 있고, views의 login에 로그인 함수 정의되어 있어
* 현재 상태에서는 form에서 입력받은거 selenium으로 넘겨서 로그인 시도하고, 성공 여부과 관계없이 chathome.html으로 넘어감 

##### 수민 )
* 로그인 실패 시 예외처리 구현했는데 더 다듬으면 좋을듯!
