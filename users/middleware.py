from django.utils import timezone

from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import UserActivity


class JWTAuthenticationInMiddleware(MiddlewareMixin):

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JWTAuthentication()
        if jwt_authentication.get_header(request):
            user, jwt = jwt_authentication.authenticate(request)
        return user


class SetLastVisitMiddleware(MiddlewareMixin):

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last-activity')
            date_now = timezone.now().isoformat()
            if not last_activity or last_activity < date_now:
                UserActivity.objects.filter(
                    username_id=request.user.id
                ).update(last_visit=timezone.now())
            request.session['last-activity'] = timezone.now().isoformat()

        return self.get_response(request)
