from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    The request is authenticated as an author, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            obj.author == request.user
        )