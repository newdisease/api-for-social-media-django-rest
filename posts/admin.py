from django.contrib import admin
from django.contrib.admin import ModelAdmin

from posts.models import Post, FavouritePost


@admin.register(Post)
class PostAdmin(ModelAdmin):
    pass


@admin.register(FavouritePost)
class FavouritePostAdmin(ModelAdmin):
    pass
