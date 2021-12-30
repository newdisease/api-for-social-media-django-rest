from django.db.models import Count, Case, When
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from posts.models import Post, FavouritePost
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer, FavouritePostSerializer


class PostViewSet(ModelViewSet):
    """Post-list & post-detail views"""
    queryset = Post.objects.all().annotate(
            likes_count=Count(Case(When(favouritepost__like=True, then=1)))).order_by('id')
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

    def perform_update(self, serializer):
        fav_post = self.get_object()
        serializer.save(like=not bool(fav_post.like))
