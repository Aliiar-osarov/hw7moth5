from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return obj.author == request.user


class OrderPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return (
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff

        return (
            request.user.is_staff
            or obj.service.author == request.user
        )