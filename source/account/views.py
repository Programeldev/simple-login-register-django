import logging
from pathlib import Path

from django.conf import settings
from django.db import models
from django.views import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import LoginForm, UserForm, UserAvatarModelForm
from .models import UserAvatarModel
from .utils import gen_html_validation_errors, get_avatar_name


log = logging.getLogger(__name__)


# Check if user is not logged
class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:index')

        return super().dispatch(request, *args, **kwargs)


# check if user is logged
class UserOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')

        return super().dispatch(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
class LoginView(GuestOnlyView, View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if settings.REMEMBER_ME:
            request.session.set_test_cookie()

        form = self.form_class()
        return render(request, self.template_name, {'login_form': form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        validation_failed = ''

        if login_form.is_valid():
            if 'remember_me' in login_form.cleaned_data:
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                    if login_form.cleaned_data['remember_me']:
                        request.session.set_expiry(settings.REMEMBER_ME_EXPIRY)
                    else:
                        request.session.set_expiry(0)

                    # pop 'remember_me' because cant be passed in authenticate()
                    login_form.cleaned_data.pop('remember_me')
                else:
                    logging.getLogger(__name__).error(
                        'Cookies don\'t work in this browser.')

            user = authenticate(**login_form.cleaned_data)

            if user is not None:
                log.info('auth ok')
                login(request, user)
                return redirect('account:index')
            else:
                log.info('auth failed')
                validation_failed = 'is-invalid'
        else:
            log.error('validation failed')
            log.error(login_form.errors.as_data())
            validation_failed = 'is-invalid'

        return render(request, self.template_name,
                  {'login_form': login_form,
                   'validation_failed': validation_failed})


class AccountView(UserOnlyView, View):
    template_name = 'account/index.html'

    def get(self, request, *args, **kwargs):
        user_form = request.user
        avatar_name = get_avatar_name(request.user)

        return render(request, self.template_name,
                      {'user_form': user_form,
                       'avatar_name': avatar_name})

    def post(self, request, *args, **kwargs):
        is_fields_invalid: dict = None
        validation_errors = ''

        if 'change-avatar-submit' in request.POST:
            user_avatar_form = UserAvatarModelForm(request.POST, request.FILES)

            if user_avatar_form.is_valid():
                user_avatar: UserAvatarModel

                try:
                    user_avatar = UserAvatarModel.objects.get(user=request.user)
                except models.ObjectDoesNotExist:
                    user_avatar = \
                        UserAvatarModel.objects.create(user=request.user)

                if user_avatar.avatar:
                    Path(user_avatar.avatar.path).unlink(missing_ok=True)

                user_avatar.avatar = \
                    user_avatar_form.cleaned_data['avatar']
                user_avatar.save()
            else:
                is_fields_invalid = {'avatar': True}

        elif 'update-account-submit' in request.POST:
            user_form = UserForm(request.POST)

            if user_form.is_valid():
                new_password = user_form.cleaned_data.pop('password')
                user_form.cleaned_data.pop('password2')

                User.objects.filter(id=request.user.id) \
                        .update(**user_form.cleaned_data)

                if new_password:
                    user = User.objects.get(pk=request.user.id)
                    user.set_password(new_password)
                    user.save()

                    user = authenticate(
                        username=user_form.cleaned_data['username'],
                        email=user_form.cleaned_data['email'],
                        password=new_password
                    )
                    login(request, user)
            else:
                log.info(user_form.cleaned_data)

                validation_errors = gen_html_validation_errors(
                                        user_form.errors.get_json_data())
                is_fields_invalid = \
                    dict.fromkeys(user_form.cleaned_data.keys(), '')
                invalid_fields = user_form.errors.as_data().keys()

                for field in invalid_fields:
                    is_fields_invalid[field] = 'is-invalid'

        user = User.objects.get(id=request.user.id)
        user_form = user
        avatar_name = get_avatar_name(request.user)

        return render(request, self.template_name,
                      {'user_form': user_form,
                       'avatar_name': avatar_name,
                       'is_fields_invalid': is_fields_invalid,
                       'validation_errors': validation_errors})


class SignUpView(GuestOnlyView, View):
    template_name = 'account:signup'

    

def logout_view(request):
    logout(request)
    return redirect('account:login')
