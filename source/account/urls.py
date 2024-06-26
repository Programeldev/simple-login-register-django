from django.urls import path

from .views import LoginView, AccountView, SignUpView, DeleteView, logout_view

app_name = 'account'

urlpatterns = [
            path('', AccountView.as_view(), name='index'),
            path('login', LoginView.as_view(), name='login'),
            path('signup', SignUpView.as_view(), name='signup'),
            path('delete', DeleteView.as_view(), name='delete'),
            path('logout', logout_view, name='logout'),
        ]
