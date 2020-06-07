from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    message = 'You are already authenticated. Please log out to try again!'

    def has_permission(self, request, view):
        # Check if the user is authenticated
        return not request.user.is_authenticated


# object-level permissions - run against operations that affect particular obj instance
# Will hide all the important update/delete API methods
class IsOwnerOrReadOnly(permissions.BasePermission):
    message  = 'You must be the owner of this content to modify!'
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
