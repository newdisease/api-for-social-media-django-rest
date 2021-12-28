from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, FavouritePost


class PostSerializer(ModelSerializer):
    """Post-list & post-detail serializers"""
    author = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'created_at', 'likes_count')

    def get_likes_count(self, instance):
        return FavouritePost.objects.filter(post=instance, like=True).count()


class FavouritePostSerializer(ModelSerializer):
    """Like serializer"""
    class Meta:
        model = FavouritePost
        fields = ('like',)
