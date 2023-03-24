from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Permisions for user in tasks"""

    def has_permission(self, request, view):
        """if user is authenticated (loggged)"""
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """If user is admin can do whatever"""
        """ if request.user.is_staff:
            return True """
        """ if not check the user owner """
        return obj.user == request.user
