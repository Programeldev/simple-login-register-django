import logging
from pathlib import Path

from django.conf import settings
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from .forms import LoginForm, UserForm, UserAvatarModelForm
from .models import UserAvatarModel
from .utils.decorators import required_login, required_guest
from .utils.gen_html_validation_errors import gen_html_validation_errors



log = logging.getLogger(__name__)


@required_guest
def login_view(request):
    login_form = LoginForm()
    validation_failed = ''

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

                    # pop 'remember_me' because no more needed
                    login_form.cleaned_data.pop('remember_me')
                else:
                    logging.getLogger(__name__).error('Cookies don\'t'
                                                    ' work in this browser.')

            user = authenticate(**login_form.cleaned_data)
            # user = authenticate(username=login_form.cleaned_data['username'],
            #                     password=login_form.cleaned_data['password'])

            if user is not None:
                log.info('auth ok')
                login(request, user)
                return redirect('account:index')
            else:
                log.info('auth nein')
                validation_failed = 'is-invalid'
        else:
            validation_failed = 'is-invalid'

    if settings.REMEMBER_ME:
        request.session.set_test_cookie()

    return render(request, 'account/login.html',
                  {'login_form': login_form,
                   'validation_failed': validation_failed})


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
                log.info('nope valid avatar')

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
