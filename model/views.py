import json

from django.http.response import HttpResponse, JsonResponse
from . import models
from . import utils
def index(request):
    return HttpResponse("hello world!")

def login(request):
    data = json.loads(request.body.decode('utf8'))
    auth_type = data.get("authType")
    email = data.get("Email")
    password = data.get("Password")
    data = {
        "status": "ok"
    }
    #402 ok
    #401 密码或者账户错误
    if auth_type == "student":
        p = models.Student.objects.get(Email=email)
        if str(p.Password) == password:
            data["status"] = 402
        else:
            data["status"] = 401
    elif auth_type == "tutor":
        p = models.Tutor.objects.filter(Email=email)
        if (str(p.getPassword()) == password):
            data["status"] = 402
        else:
            data["status"] = 401
    elif auth_type == "admin":
        p = models.Administer.objects.filter(Email=email)
        if (p.Password == password):
            data["status"] = 402
        else:
            data["status"] = 401
    if data["status"] == 402:
        request.session['auth_type'] = auth_type
        request.session['userEmail'] = email

    return JsonResponse(data)

def sign(request):
    print(request.POST)
    auth_type = str(request.POST.get("authType"))
    name = str(request.POST.get('Name'))
    school = str(request.POST.get('School'))
    email = str(request.POST.get("Email"))
    password = str(request.POST.get("Password"))
    majority = str(request.POST.get('Majority'))
    data = {
        "status": 0
    }
    #401表示邮箱无效（不是edu或者已经被注册了） 402表示ok
    #403表示密码格式不对，目前的格式只做了长度约束，6-26
    if not utils.validate_email(str(email)):
        print(str(email))
        data["status"] = 401
        print('i am in 1')
    elif not utils.check_password(str(password)):
        data["status"] = 403
        print('i am in 2')
    elif auth_type == "student":
        if models.Student.objects.filter(Email=email).exists():
            data["status"] = 401
            print('i am in 3')
        else:
            models.Student.objects.create(
                Name=name,
                School=school,
                Email=email,
                Password=password,
                Majority=majority,
                ScientificExperience="1234",
            )
            data["status"] = 402
            print('i am in 4')
    elif auth_type == "tutor":
        if models.Tutor.objects.filter(Email=email).exists():
            data["status"] = 401
            print('i am in 5')
        else:
            models.Tutor.objects.create(
                Name=name,
                School=school,
                Email=email,
                Password=password,
                Majority=majority,
            )
            data["status"] = 402
            print('i am in 6')
    return JsonResponse(data)
