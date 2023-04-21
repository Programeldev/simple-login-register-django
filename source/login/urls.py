from django.urls import path

from .views import login


app_name = 'login'

urlpatterns = [
            path('login.html', login, name='login')
        ]
