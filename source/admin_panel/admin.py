from django.contrib import admin
from django.contrib.auth.models import User

from .forms import AuthenticationPanelForm
from account.models import UserAvatarModel


class AdminPanel(admin.AdminSite):
    login_form = AuthenticationPanelForm


class ModelAdmin(admin.ModelAdmin):
    pass


admin_site = AdminPanel()
admin_site.register(User, ModelAdmin)
admin_site.register(UserAvatarModel, ModelAdmin)
