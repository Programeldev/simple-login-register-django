from django.urls import path

from .views import login_view


app_name = 'account'

urlpatterns = [
            path('login.html', login_view)
        ]
