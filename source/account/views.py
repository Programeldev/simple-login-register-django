from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.views.generic.edit import FormView
# from django.contrib.auth.decorators import login_required

from .forms import UserForm
from django import forms


def login_view(request):
    if request.user.is_authenticated:
        return redirect('account:index')

    user_form = UserForm()

    if request.method == 'POST':
        if request.session.test_cookie_worked():
            # if user_form.cleaned_data[]
            request.session.delete_test_cookie()

        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = authenticate(**user_form.cleaned_data)

            if user is not None:
                login(request, user)
                return redirect('account:index')

    if settings.REMEMBER_ME:
        request.session.set_expiry(settings.REMEMBER_ME_EXPIRY)
        request.session.set_test_cookie()

    return render(request, 'account/login.html', {'user_form': user_form})


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('account:login')

    return render(request, 'account/index.html') 


def logout_view(request):
    logout(request)
    return redirect('account:login') 
