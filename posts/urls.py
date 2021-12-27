from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet

app_name = 'posts'

router = SimpleRouter()

router.register(r'posts', PostViewSet)

urlpatterns = []

urlpatterns += router.urls
