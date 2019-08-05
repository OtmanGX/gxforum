from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetView

from authenticate.views import LoginFormView, LogoutFormView
from . import views

urlpatterns = [
    path('login/', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutFormView.as_view(), name="logout"),
    path('register/', views.SignUpView.as_view(), name="register"),
    path('edit/profile', views.EditProfileView.as_view(), name="edit_profile"),
    path('edit/password', views.change_password, name="password"),
    url(r'^reset/$',PasswordResetView.as_view(
        template_name='reset/password_reset.html',
        email_template_name='reset/password_reset_email.html',
        subject_template_name='reset/password_reset_subject'
    ), name='password_reset'),
    url(r'^reset/done/$',
        PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),name='password_reset_confirm'),
    url(r'^reset/complete/$',
        PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),name='password_reset_complete'),
    # path('edit/password', views.ChangePasswordView.as_view(), name="password"),
]
