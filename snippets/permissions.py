"""
Custom permissions for the snippets app.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Returns whether the user is the owner for unsafe methods,
        True otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user