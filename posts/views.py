import datetime

from django.db.models import Count, Case, When
from rest_framework import views
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from posts.models import Post, FavouritePost
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer, FavouritePostSerializer


class PostViewSet(ModelViewSet):
    """CRUD functional for posts"""
    queryset = Post.objects.all().annotate(
        likes_count=Count(Case(When(favouritepost__like=True, then=1)))).select_related('author').order_by('id')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()


class FavouritePostView(UpdateModelMixin, GenericViewSet):
    """Makes like and unlike to post"""
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


class LikesAnalyticsView(views.APIView):
    """Shows likes in date range"""

    def get(self, request):
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if not date_to:
            date_to = datetime.datetime.now()
        all_likes = FavouritePost.objects.filter(like=True, date__range=[date_from, date_to]).count()
        return Response({"likes-stat": all_likes})
