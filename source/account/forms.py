import logging

from django import forms
from django.conf import settings

from .models import UserAvatarModel
from .validators import name_validators, password_validators, \
                        username_validators, email_validators


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        if settings.USE_USERNAME:
            self.fields['username'] = forms.CharField(validators=username_validators)

        if settings.USE_EMAIL:
            self.fields['email'] = forms.EmailField(validators=email_validators)

        # Make sure if at least one option is selected from above.
        # If not, add username field for default.
        if not settings.USE_USERNAME and not settings.USE_EMAIL:
            self.fields['username'] = forms.CharField(validators=username_validators)

            logging.getLogger(__name__).info('At least one of username or '
                                             'email field must be select. '
                                             'Selected username field for '
                                             'default.')

        self.fields['password'] = forms.CharField(widget=forms.PasswordInput,
                                                  validators=password_validators)
        # self.fields['password'] = forms.CharField(widget=forms.PasswordInput)

        if settings.REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(required=False)


class UserForm(forms.Form):
    first_name = forms.CharField(validators=name_validators, required=False)
    last_name = forms.CharField(validators=name_validators, required=False)
    username = forms.CharField(validators=username_validators, required=False)
    email = forms.EmailField(validators=email_validators, required=False)
    # password = forms.CharField(widget=forms.PasswordInput,
    #                            validators=password_validators,
    #                            required=False)


class UserAvatarModelForm(forms.ModelForm):
    class Meta:
        model = UserAvatarModel
        fields = ['avatar']
