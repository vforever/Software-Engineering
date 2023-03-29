from django.http.response import HttpResponse, JsonResponse
from models import *
from utils import *
def index(request):
    return HttpResponse("hello world!")

def login(request):
    auth_type = request.POST.get("authType")
    email = request.POST.get("Email")
    password = request.POST.get("Password")
    data = {
        "status": 0
    }
    #402 ok
    #401 密码或者账户错误
    if auth_type == "student":
        p = Student.objects.filter(Email=email)
        if (p.Password == password):
            data["status"] = 402
        else:
            data["status"] = 401
    elif auth_type == "tutor":
        p = Tutor.objects.filter(Email=email)
        if (p.Password == password):
            data["status"] = 402
        else:
            data["status"] = 401
    elif auth_type == "admin":
        p = Administer.objects.filter(Email=email)
        if (p.Password == password):
            data["status"] = 402
        else:
            data["status"] = 401
    ##TODO:这里写得比较粗糙，直接存了type和email，实际上应该存ID
    if data["status"] == 402:
        request.session['auth_type'] = auth_type
        request.session['userEmail'] = email

    return JsonResponse(data)

def sign(request):
    auth_type = request.POST.get("authType")
    name = request.POST.get('Name')
    school = request.POST.get('School')
    email = request.POST.get("Email")
    password = request.POST.get("Password")
    majority = request.POST.get('Majority')
    data = {
        "status":0
    }
    #401表示邮箱无效（不是edu或者已经被注册了） 402表示ok
    #403表示密码格式不对，目前的格式只做了长度约束，6-26
    if not validate_email(email):
        data["status"] = 401
    elif not check_password(password):
        data["status"] = 403
    elif auth_type == "student":
        if Student.objects.filter(Email=email).exists():
            data["status"] = 401
        else:
            Student.objects.create(
                Name=name,
                School=school,
                Email=email,
                Password=password,
                Majority=majority,
            )
            data["status"] = 402
    elif auth_type == "tutor":
        if Tutor.objects.filter(Email=email).exists():
            data["status"] = 401
        else:
            Tutor.objects.create(
                Name=name,
                School=school,
                Email=email,
                Password=password,
                Majority=majority,
            )
            data["status"] = 402
    return JsonResponse(data)
