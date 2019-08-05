from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy


class LoginFormView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    success_message = "You were successfully logged in"


class LogoutFormView(SuccessMessageMixin, LogoutView):
    success_message = "You were successfully logged out"

    def get(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().get(self, request, *args, **kwargs)


class SignUpView(CreateView):
    template_name = "register.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")


class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "profile.html"
    model = User
    form_class = EditProfileForm
    success_url = reverse_lazy("edit_profile")
    success_message = "The data has been updated !"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


@login_required
def change_password(request):
    success_message = "The data has been updated !"
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, success_message)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password.html', {'form': form})
