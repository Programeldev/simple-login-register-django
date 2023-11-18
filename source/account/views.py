from django.http import HttpResponseRedirect, HttpResponse
from django.forms import modelformset_factory
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required

from .forms import UserForm
from django import forms


def login_view(request):
    if request.user.is_authenticated:
        print('zalogowany')
        return redirect('account:index')

    user_form = UserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            auth_kwargs = {
                'username': user_form.cleaned_data['username'],
                'password': user_form.cleaned_data['password']
            }

            if settings.EMAIL:
                auth_kwargs.update({'email': user_form.cleaned_data['email']})

            user = authenticate(**auth_kwargs)
            if user is not None:
                login(request, user)
                return redirect('account:index')

    return render(request, 'account/login.html', {'user_form': user_form})


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('account:login')

    return render(request, 'main.html') 


def logout_view(request):
    logout(request)

    return HttpResponseRedirect() 
