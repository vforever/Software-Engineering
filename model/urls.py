from django.urls import path

from . import views

urlpatterns = [
    path('home', views.index),
    path('kk', views.kk),
    path('login', views.login)
]
