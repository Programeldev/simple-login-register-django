from django.urls import path

from .views import account_view, login_view, logout_view #, change_avatar_view

app_name = 'account'

urlpatterns = [
            path('', account_view, name='index'),
            path('login', login_view, name='login'),
            path('logout', logout_view, name='logout'),
            # path('change_avatar', change_avatar_view, name='change_avatar'),
        ]
