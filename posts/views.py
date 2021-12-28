from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from posts.models import Post, FavouritePost
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer, FavouritePostSerializer


class PostViewSet(ModelViewSet):
    """Post-list & post-detail views"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class FavouritePostView(UpdateModelMixin, GenericViewSet):
    """Like posts view"""
    permission_classes = [IsAuthenticated]
    queryset = FavouritePost.objects.all()
    serializer_class = FavouritePostSerializer
    lookup_field = 'post'

    def get_object(self):
        obj, _ = FavouritePost.objects.get_or_create(
            user=self.request.user,
            post_id=self.kwargs['post']
        )
        return obj
