from django.contrib.auth.models import User
from django.conf import settings
from django import forms


class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        if settings.USE_USERNAME:
            self.fields['username'] = forms.CharField(label='Username',
                                                      min_length=4, 
                                                      max_length=150)

        if settings.USE_EMAIL:
            self.fields['email'] = forms.EmailField(max_length=150)


        self.fields['password'] = forms.CharField(min_length=8,
                                                  max_length=150, 
                                                  widget=forms.PasswordInput)
