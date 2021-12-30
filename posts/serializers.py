from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, FavouritePost


class PostSerializer(ModelSerializer):
    """Post-list & post-detail serializers"""
    author = serializers.StringRelatedField()
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'author', 'created_at', 'likes_count')


class FavouritePostSerializer(ModelSerializer):
    """Like serializer"""

    class Meta:
        model = FavouritePost
        fields = ('post', 'like',)
