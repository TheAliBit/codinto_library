from rest_framework.permissions import BasePermission


class IsNotSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id != request.user.id
