from django.urls import path

from .views import views

urlpatterns = [
    path('register', views.sign),
    path('login', views.login),
    path('sendCheckCode', views.sendEmail)
]
