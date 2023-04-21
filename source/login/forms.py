import django.forms

class LoginForm(django.forms.Form):
    username = django.forms.CharField(label='Username', max_length=255)
    email = django.forms.EmailField(max_length=255)
