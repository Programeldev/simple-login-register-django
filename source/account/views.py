import logging

# from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
# from django.contrib.auth.models import User
# from django.views.generic.base import View
# from django.views.generic.edit import FormView

from .forms import LoginForm, UserForm, UserAvatarModelForm
from .utils.decorators import required_login, required_guest
from .utils.gen_html_validation_errors import gen_html_validation_errors


@required_guest
def login_view(request):
    login_form = LoginForm()
    validation_failed: str = None

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

            logging.getLogger(__name__).info(login_form.cleaned_data)
            user = authenticate(**login_form.cleaned_data)

            if user is not None:
                login(request, user)
                return redirect('account:index')
            else:
                logging.getLogger(__name__).error('no logged')
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
    is_fields_valid = {}
    validation_errors = {}
    log = logging.getLogger(__name__)

    if request.method == "POST":
        if 'change-avatar-submit' in request.POST:
            log.info('change avatar')

        elif 'update-account-submit' in request.POST:
            log.info('change account')
            user_form = UserForm(request.POST)

            if user_form.is_valid():
                log.info('everything is correct!')
            else:
                validation_errors = gen_html_validation_errors(
                                        user_form.errors.get_json_data())
                is_fields_valid = dict.fromkeys(user_form.cleaned_data.keys())
                invalid_fields = user_form.errors.as_data().keys()

                for field in invalid_fields:
                    is_fields_valid[field] = 'is-invalid'

                log.error('validation failed!')

    user_form = get_user(request)

    return render(request, 'account/index.html',
                  {'user_form': user_form,
                   'is_fields_valid': is_fields_valid,
                   'validation_errors': validation_errors})


def logout_view(request):
    logout(request)
    return redirect('account:login')


# @required_login
# def change_avatar_view(request):
#     pass
