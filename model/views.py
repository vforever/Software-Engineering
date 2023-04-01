import json
import math
import random
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache
from . import models
from . import utils
from . import sendEmial
from . import token


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
            response["msg"] = "密码有误，请重新输入！"
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
            response["msg"] = "密码有误，请重新输入！"
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
    response["msg"] = "用户名不存在！"
    return JsonResponse(response)


def sign(request):
    data = json.loads(request.body)
    name = data.get("username")
    userType = data.get("userType")
    school = data.get("university")
    email = data.get("userId")
    password = data.get("password")
    checkCode = data.get("checkCode")
    response = {
        "result": 0,
        "msg": ""
    }
    check = cache.get(f"{email}+{checkCode}", default="!")
    if userType == "student":
        students = models.Student.objects.filter(Email=email)
        if students.exists():
            response["msg"] = "该邮箱已被注册！"
        elif ~students.exists():
            if check == checkCode:
                student = models.Student(
                    Name=name,
                    School=school,
                    Email=email,
                    Password=password
                )
                student.save()
                response["result"] = 1
                response["msg"] = "注册成功"
            elif check != checkCode:
                response["msg"] = "验证码不正确！"
    elif userType == "teacher":
        tutors = models.Tutor.Objects.filter(Email=email)
        if tutors.exists():
            response["msg"] = "该邮箱已被注册！"
        elif ~tutors.exists():
            if check == checkCode:
                tutor = models.Tutor(
                    Name=name,
                    School=school,
                    Email=email,
                    Password=password
                )
                tutor.save()
                response["result"] = 1
                response["msg"] = "注册成功"
            elif check != checkCode:
                response["msg"] = "验证码不正确！"
    '''
    elif userType == "admin":
    '''
    return JsonResponse(response)


def sendEmail(request):
    data = json.loads(request.body)
    email = data.get("email")
    response = {
        "result": 0,
        "msg": "验证码发送失败，请重新尝试！"
    }
    #邮件主题
    subject = u'注册验证码'
    verifyKey = math.floor(1e5 * random.random())
    cache.set(f"{email}+{verifyKey}", str(verifyKey), 180)
    t = f"your verify key is {verifyKey}"
    html_content = str(t)
    #收件人列表
    to_list = [email, ]
    #根据模版发送邮件
    result = sendEmial.send_html_email(subject, html_content, to_list)
    if result:
        response["result"] = 1
        response["msg"] = "验证码已发送到给定邮箱"
    return JsonResponse(response)

