import logging

from django import forms
from django.conf import settings
from django.contrib.auth.models import User

from .models import UserAvatarModel
from .validators import name_validators, password_validators, \
                        username_validators, email_validators

log = logging.getLogger(__name__)

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        if settings.USE_USERNAME:
            self.fields['username'] = forms.CharField(validators=username_validators)

        if settings.USE_EMAIL:
            self.fields['email'] = forms.EmailField(validators=email_validators)

        # Make sure if at least one option is selected from above.
        # If not, add username field for default.
        if not settings.USE_USERNAME and not settings.USE_EMAIL:
            self.fields['username'] = forms.CharField(validators=username_validators)

            logging.getLogger(__name__).info(
                'At least one of username or email field must be select.'
                ' Selected username field for default.')

        self.fields['password'] = forms.CharField(widget=forms.PasswordInput,
                                                  validators=password_validators)


class LoginForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(required=False)


class SignUpForm(BaseForm):
    password2 = forms.CharField(widget=forms.PasswordInput,
                                validators=password_validators)

    def clean(self):
        cleaned_data = super().clean()
        users = User.objects.all()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if not password == password2:
            self.add_error('password',
                           'Passed passwords is different !')

        try:
            username = cleaned_data['username']

            if users.filter(username=username).exists():
                self.add_error('username',
                               'This username is used by someone.')
        except KeyError:
            pass

        try:
            email = cleaned_data['email']

            if users.filter(email=email).exists():
                self.add_error('email',
                               'This email is used by someone.')
        except KeyError:
            pass
        #
        # if hasattr(self, 'username'):
        #     log.info('filed username')
        #     username = cleaned_data['username']
        #
        #     if users.filter(username=username).exists():
        #         self.add_error('username',
        #                        'This username is used by someone.')
        #
        # if hasattr(self, 'email'):
        #     log.info('filed email')
        #     email = cleaned_data['email']
        #
        #     if users.filter(email=email).exists():
        #         self.add_error('username',
        #                        'This email is used by someone.')


class UserForm(forms.Form):
    first_name = forms.CharField(validators=name_validators, required=False)
    last_name = forms.CharField(validators=name_validators, required=False)
    username = forms.CharField(validators=username_validators, required=False)
    email = forms.EmailField(validators=email_validators, required=False)
    password = forms.CharField(widget=forms.PasswordInput,
                               validators=password_validators,
                               required=False)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                validators=password_validators,
                                required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if not password == password2:
            self.add_error('password',
                           'Passed passwords is different !')


class UserAvatarModelForm(forms.ModelForm):
    class Meta:
        model = UserAvatarModel
        fields = ['avatar']
