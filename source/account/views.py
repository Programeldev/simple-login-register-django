import logging
from pathlib import Path

from django.conf import settings
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views import View

from .forms import LoginForm, UserForm, UserAvatarModelForm
from .models import UserAvatarModel
from .utils.decorators import required_login, required_guest
from .utils.gen_html_validation_errors import gen_html_validation_errors


log = logging.getLogger(__name__)


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:index')

        return super().dispatch(request, *args, **kwargs)


class LoginView(GuestOnlyView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if settings.REMEMBER_ME:
            request.session.set_test_cookie()

        form = self.form_class()
        log.info(self.template_name)
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
                    log.error('Cookies don\'t work in this browser.')

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

# @required_guest
# def login_view(request):
#     login_form = LoginForm()
#     validation_failed = ''
#
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#
#         if login_form.is_valid():
#             if 'remember_me' in login_form.cleaned_data:
#                 if request.session.test_cookie_worked():
#                     request.session.delete_test_cookie()
#
#                     if login_form.cleaned_data['remember_me']:
#                         request.session.set_expiry(settings.REMEMBER_ME_EXPIRY)
#                     else:
#                         request.session.set_expiry(0)
#
#                     # pop 'remember_me' because cant be passed in authenticate()
#                     login_form.cleaned_data.pop('remember_me')
#                 else:
#                     log.error('Cookies don\'t work in this browser.')
#
#             user = authenticate(**login_form.cleaned_data)
#
#             if user is not None:
#                 log.info('auth ok')
#                 login(request, user)
#                 return redirect('account:index')
#             else:
#                 log.info('auth failed')
#                 validation_failed = 'is-invalid'
#         else:
#             log.error('validation failed')
#             log.error(login_form.errors.as_data())
#             validation_failed = 'is-invalid'
#
#     if settings.REMEMBER_ME:
#         request.session.set_test_cookie()
#
#     return render(request, 'account/login.html',
#                   {'login_form': login_form,
#                    'validation_failed': validation_failed})
#

class AccountView(LoginRequiredMixin, View):
    template_name = 'account/index.html'
    login_url = 'account/login'
    redirect_field_name = 'account/'
    user_avatar: UserAvatarModel
    avatar_name: str

    def dispatch(self, request, *args, **kwargs):
        try:
            user_avatar = UserAvatarModel.objects.get(user=request.user)
            self.avatar_name = user_avatar.avatar.name
        except models.ObjectDoesNotExist:
            self.avatar_name = None

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.user_form = request.user
        return render(request, self.template_name,
                      {'user_form': self.user_form,
                       'avatar_name': self.avatar_name})

    def post(self, request, *args, **kwargs):
        is_fields_invalid: dict = None
        validation_errors = ''

        if 'change-avatar-submit' in request.POST:
            user_avatar_form = UserAvatarModelForm(request.POST, request.FILES)
            if user_avatar_form.is_valid():
                if self.avatar_name:
                    # Delete old avatar from BASE_DIR/media/
                    Path(self.user_avatar.avatar.path).unlink(missing_ok=True)

                    # Updating avatar to new
                    self.user_avatar.avatar = \
                        user_avatar_form.cleaned_data['avatar']
                    self.user_avatar.save()
                    self.avatar_name = self.user_avatar.avatar.name
                else:
                    self.user_avatar = \
                        UserAvatarModel.objects.create(user=request.user,
                                avatar=user_avatar_form.cleaned_data['avatar'])
                    self.avatar_name = self.user_avatar.avatar.name
            else:
                is_fields_invalid = {'avatar': True}

        elif 'update-account-submit' in request.POST:
            user_form = UserForm(request.POST)

            if user_form.is_valid():
                log.info(user_form.cleaned_data)
                User.objects.filter(id=request.user.id) \
                            .update(**user_form.cleaned_data)

                # Updating user data for render context
                self.user_form = User.objects.get(id=request.user.id)
            else:
                validation_errors = gen_html_validation_errors(
                                        user_form.errors.get_json_data())
                is_fields_invalid = \
                        dict.fromkeys(user_form.cleaned_data.keys(), '')
                invalid_fields = user_form.errors.as_data().keys()

                for field in invalid_fields:
                    is_fields_invalid[field] = 'is-invalid'

        return render(request, self.template_name,
                      {'user_form': self.user_form,
                       'avatar_name': self.avatar_name,
                       'is_fields_invalid': is_fields_invalid,
                       'validation_errors': validation_errors,})


@required_login
def account_view(request):
    is_fields_valid: dict = None
    validation_errors = ''
    user_avatar: UserAvatarModel = None
    avatar_name: str = None

    try:
        user_avatar = UserAvatarModel.objects.get(user=request.user)
        avatar_name = user_avatar.avatar.name
    except models.ObjectDoesNotExist:
        avatar_name = None

    if request.method == "POST":
        if 'change-avatar-submit' in request.POST:
            user_avatar_form = UserAvatarModelForm(request.POST, request.FILES)
            if user_avatar_form.is_valid():
                if avatar_name:
                    # Delete old avatar from BASE_DIR/media/
                    Path(user_avatar.avatar.path).unlink(missing_ok=True)

                    # Updating avatar to new
                    user_avatar.avatar = \
                        user_avatar_form.cleaned_data['avatar']
                    user_avatar.save()
                    avatar_name = user_avatar.avatar.name
                else:
                    user_avatar = \
                        UserAvatarModel.objects.create(user=request.user,
                                avatar=user_avatar_form.cleaned_data['avatar'])
                    avatar_name = user_avatar.avatar.name
            else:
                is_fields_valid = {'avatar': True}

        elif 'update-account-submit' in request.POST:
            user_form = UserForm(request.POST)

            if user_form.is_valid():
                log.info(user_form.cleaned_data)
                User.objects.filter(id=request.user.id) \
                            .update(**user_form.cleaned_data)
            else:
                validation_errors = gen_html_validation_errors(
                                        user_form.errors.get_json_data())
                is_fields_valid = \
                        dict.fromkeys(user_form.cleaned_data.keys(), '')
                invalid_fields = user_form.errors.as_data().keys()

                for field in invalid_fields:
                    is_fields_valid[field] = 'is-invalid'

    user_form = request.user

    return render(request, 'account/index.html',
                  {'user_form': user_form,
                   'is_fields_valid': is_fields_valid,
                   'validation_errors': validation_errors,
                   'avatar_name': avatar_name})


def logout_view(request):
    logout(request)
    return redirect('account:login')


# @required_login
# def change_avatar_view(request):
#     pass
