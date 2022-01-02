from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(ModelAdmin):
    pass
