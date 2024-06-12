from django.urls import path, include
from admin_panel.admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('account/', include('account.urls'))
]
