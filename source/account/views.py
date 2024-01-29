import logging


from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.views.generic.edit import FormView

from .forms import LoginForm, UserForm, UserAvatarModelForm
from .utils.decorators import required_login, required_guest

@required_guest
def login_view(request):
    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            if 'remember_me' in login_form.cleaned_data:
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                    if login_form.cleaned_data['remember_me']:
                        request.session.set_expiry(settings.REMEMBER_ME_EXPIRY)
                    else:
                        request.session.set_expiry(0)
                    
                    login_form.cleaned_data.pop('remember_me')

            user = authenticate(**login_form.cleaned_data)

            if user is not None:
                login(request, user)
                return redirect('account:index')

    if settings.REMEMBER_ME:
        request.session.set_test_cookie()

    return render(request, 'account/login.html', {'login_form': login_form})


@required_login
def account_view(request):
    log = logging.getLogger()
    if request.method == "POST":
        if 'change-avatar-submit' in request.POST:
            log.info('change avatar')

        elif 'update-account-submit' in request.POST:
            pass

    user_form = get_user(request)
    # us = UserModelForm()

    return render(request, 'account/index.html', {'user_form': user_form}) 


def logout_view(request):
    logout(request)
    return redirect('account:login') 


@required_login
def change_avatar_view(request):
    pass
