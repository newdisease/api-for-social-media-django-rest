from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostSerializer(ModelSerializer):
    """Post-list & post-detail serializers"""
    class Meta:
        model = Post
        fields = '__all__'
