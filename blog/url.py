from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.PostsListView.as_view(), name='index_blog'),
    path('<str:slug>/', views.PostDetailView.as_view(), name='blog'),
]
