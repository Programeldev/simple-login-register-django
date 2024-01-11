from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.views.generic.edit import FormView

from .forms import UserForm, UserAvatarModelForm
from django import forms


def required_login(func):
    """ Decorator to check if user is logged. """
    def inner(request):
        if not request.user.is_authenticated:
            return redirect('account:login')

        ret = func(request)
        return ret
    
    return inner


def login_view(request):
    # checking if user is logged
    if request.user.is_authenticated:
        return redirect('account:index')

    user_form = UserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            if 'remember_me' in user_form.cleaned_data:
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                    if user_form.cleaned_data['remember_me']:
                        request.session.set_expiry(settings.REMEMBER_ME_EXPIRY)
                    else:
                        request.session.set_expiry(0)
                    
                    user_form.cleaned_data.pop('remember_me')

            user = authenticate(**user_form.cleaned_data)

            if user is not None:
                login(request, user)
                return redirect('account:index')

    if settings.REMEMBER_ME:
        request.session.set_test_cookie()

    return render(request, 'account/login.html', {'user_form': user_form})


@required_login
def account_view(request):
    if request.method == "POST":
        if 'avatar' in request.FILES:
            print('avatar')

        # user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            print('user')
        

    user_form = get_user(request)

    return render(request, 'account/index.html', {'user_form': user_form}) 


def logout_view(request):
    logout(request)
    return redirect('account:login') 


@required_login
def change_avatar_view(request):
    pass
