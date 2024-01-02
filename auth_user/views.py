from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from auth_user.forms import UserRegistrationForm
from django.views.generic import  FormView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'auth_user/user_registration_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # print(form.cleaned_data)
        user=form.save()
        login(self.request, user)
        # print(user)

        messages.success(self.request, f'Account Successfully Created')
        return super().form_valid(form) # form_valid function call hobe jodi sob thik thake


class UserLoginView(LoginView):
    template_name = 'auth_user/user_login.html'
    def get_success_url(self):
        messages.success(self.request ,'Logged in Successfully')
        return reverse_lazy('home')

class UserLogoutView(View):
    
    def get(self, request):
        logout(request)
        messages.success(self.request ,'Logged Out Successfully')
        return redirect('home')

