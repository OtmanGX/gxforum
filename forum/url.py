"""gxforum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

app_name = "forum"


urlpatterns = [
    path('', views.BoardListView.as_view(), name='index'),
    path('board/<int:pk>/', views.TopicListView.as_view(), name='board'),
    path('board/<int:id>/new', views.NewPostView.as_view(), name='new_topic'),
    path('post/<int:post_uk>/edit', views.EditPostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='delete_post'),
    path('board/<int:id>/topic/<int:topic_id>', views.PostsListView.as_view(), name='topic'),
]
