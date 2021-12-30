from django.urls import path
from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, FavouritePostView, LikesAnalyticsView

app_name = 'posts'

router = SimpleRouter()

router.register(r'posts', PostViewSet)
router.register(r'like', FavouritePostView)

urlpatterns = [
    path('analytics/', LikesAnalyticsView.as_view()),
]

urlpatterns += router.urls
