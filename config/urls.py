from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')),
    path('api/v1/auth', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
