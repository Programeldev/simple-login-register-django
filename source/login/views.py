from django.http import HttpResponseRedirect, HttpResponse
from django.forms import modelformset_factory
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .forms import UserForm
from django import forms


def login_view(request):
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

            if authenticate(**auth_kwargs):
                return HttpResponseRedirect('/account')

    return render(request, 'login/login.html', {'user_form': user_form})
