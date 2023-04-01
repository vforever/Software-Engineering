from django.urls import path

from . import views

urlpatterns = [
    path('home', views.index),
    path('sign', views.sign),
    path('login', views.login),
    path('email', views.sendEmail)
]
