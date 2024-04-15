from django.urls import path

from .views import account_view, logout_view, LoginView, AccountView

app_name = 'account'

urlpatterns = [
            path('', AccountView.as_view(), name='index'),
            # path('', account_view, name='index'),
            # path('login', login_view, name='login'),
            path('login', LoginView.as_view(), name='login'),
            path('logout', logout_view, name='logout'),
        ]
