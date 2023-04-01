import json
<<<<<<< HEAD

from django.http.response import JsonResponse
from . import models
from . import utils
from . import token

=======
import math, random
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from . import models
from . import utils
from . import sendEmial
def index(request):
    return HttpResponse("hello world!")
>>>>>>> c834234cd5a342089673cfc2588bd1109629f054

def login(request):
    data = json.loads(request.body)
    email = data.get("userId")
    password = data.get("password")
    response = {
        "result": 0,
        "token": "",
        "msg": "",
        "userType": ""
    }
    students = models.Student.objects.filter(Email=email)
    tutors = models.Tutor.objects.filter(Email=email)
    # admins = models.Administer.objects.filter(Email=email)
    if students.exists():
        student = models.Student.objects.get(Email=email)
        if student.Password == password:
            response["result"] = 1
            response["token"] = token.create_token(email)
            response["msg"] = "登录成功"
            response["userType"] = "student"
        elif student.Password != password:
            response["result"] = 0
            response["msg"] = "密码有误!"
            response["userType"] = "student"
        return JsonResponse(response)
    elif tutors.exists():
        tutor = models.Tutor.objects.get(Email=email)
        if tutor.Password == password:
            response["result"] = 1
            response["token"] = token.create_token(email)
            response["msg"] = "登录成功"
            response["userType"] = "teacher"
        elif tutor.Password != password:
            response["result"] = 0
            response["msg"] = "密码有误!"
            response["userType"] = "teacher"
        return JsonResponse(response)
    ''' 管理员登录  
    elif admins.exists():
        admin = models.Administer.objects.get(Email=email)
        if admin.Password == password:
            response["result"] = 1
            response["token"] = token.create_token(email)
            response["msg"] = "登录成功"
            response["userType"] = "admin"
        elif tutor.Password != password:
            response["result"] = 0
            response["msg"] = "密码有误!"
            response["userType"] = "admin"
        return JsonResponse(response)
    '''
    response["msg"] = "用户名不存在!"
    return JsonResponse(response)


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
<<<<<<< HEAD
    return JsonResponse(data)
=======
    return JsonResponse(data)

def sendEmail(request):
    #邮件主题
    subject = u'注册验证码'
    verifyKey = math.floor(1e5 * random.random())
    t = f"your verify key is {verifyKey}"
    html_content = str(t)
    #收件人列表
    to_list = ['2306164338@qq.com', ]
    #根据模版发送邮件
    result = sendEmial.send_html_email(subject, html_content, to_list)
    data = {
        "status": result
    }
    return HttpResponse("Hello")

>>>>>>> c834234cd5a342089673cfc2588bd1109629f054
