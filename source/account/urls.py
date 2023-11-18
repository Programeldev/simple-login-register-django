from django.urls import path

from .views import login_view, account_view

app_name = 'account'

urlpatterns = [
            path('', account_view, name='index'),
            path('login', login_view, name='login')
        ]
