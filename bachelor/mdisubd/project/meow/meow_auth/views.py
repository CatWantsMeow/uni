from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from meow_auth.forms import LoginForm, LandlordRegistrationForm, TenantRegistrationForm
from meow_auth.db import login, register_landlord, register_tenant, logout
from meow_main.views import UserViewMixin


class LoginView(UserViewMixin, TemplateView):

    template_name = 'meow_auth/login.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_id, token = login(username, password)
            if user_id < 0:
                form.add_error('username', 'Wrong username or password')
                form.add_error('password', 'Wrong username or password')
            else:
                old_token = request.COOKIES.get('token', None)
                logout(old_token)
                response = redirect('mall-list')
                response.set_cookie('token', token)
                response.set_cookie('user_id', user_id)
                return response

        context = self.get_context_data(**kwargs)
        context['login_form'] = form
        return render(request, self.template_name, context=context)


class RegistrationView(UserViewMixin, TemplateView):

    template_name = 'meow_auth/registration.html'
    form_class = None
    register_function = None

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['registration_form'] = self.form_class()
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            registered = self.register_function.im_func(form.cleaned_data)
            if registered:
                return redirect('login')
            else:
                form.add_error('username', 'User with specified username already exists')

        context = self.get_context_data(**kwargs)
        context['registration_form'] = form
        return render(request, self.template_name, context=context)


class LandlordRegistrationView(RegistrationView):

    form_class = LandlordRegistrationForm
    register_function = register_landlord


class TenantRegistrationView(RegistrationView):

    form_class = TenantRegistrationForm
    register_function = register_tenant


class LogoutView(TemplateView):

    def get(self, request, **kwargs):
        old_token = request.COOKIES.get('token', None)
        logout(old_token)
        response = redirect('/')
        response.delete_cookie('token')
        return response
