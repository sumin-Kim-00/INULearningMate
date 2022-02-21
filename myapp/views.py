from django.shortcuts import render, HttpResponse

# 첫 번째 파라미터로 요청과 관련된 여러가지 정보가 들어있는 객체를 전달해주도록 되어있음(request)

def home(request):
    context = {}

    return render(request, "chathome.html", context)



"""
def index(request):
    return HttpResponse('<h1>Random</h1>' + str(random.random()))  # Http를 이용해서 응답

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read!' + id )
"""