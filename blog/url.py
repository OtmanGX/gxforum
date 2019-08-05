from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index_blog'),
    path('<str:slug>/', views.post, name='blog'),
]
