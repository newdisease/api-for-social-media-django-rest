from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, FavouritePostView

app_name = 'posts'

router = SimpleRouter()

router.register(r'posts', PostViewSet)
router.register(r'like', FavouritePostView)

urlpatterns = []

urlpatterns += router.urls
