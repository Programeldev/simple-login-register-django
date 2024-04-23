from django.urls import path

from .views import logout_view, LoginView, AccountView

app_name = 'account'

urlpatterns = [
            path('', AccountView.as_view(), name='index'),
            path('login', LoginView.as_view(), name='login'),
            path('logout', logout_view, name='logout'),
        ]
