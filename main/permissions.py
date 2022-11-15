from rest_framework import permissions
from accounts.enums import UserRoles

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        pass


    def has_object_permission(self, request, view, obj):
        return obj.client == request.user


class DirectorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.director.value


class IsnotclientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role != UserRoles.client.value


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRoles.client.value


class Orderpermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == UserRoles.client.value:
            if request.method == "get":
                return