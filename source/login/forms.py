from django.contrib.auth.models import User
from django.conf import settings
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=150)
    password = forms.CharField(min_length=8, max_length=150, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        if settings.EMAIL: 
            self.fields['email'] = forms.EmailField(max_length=150)
