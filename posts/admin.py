from django.contrib import admin
from django.contrib.admin import ModelAdmin

from posts.models import Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    pass
