from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.conf import settings


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.username == settings.OWNER_USERNAME


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # leitura liberada
        if request.method in SAFE_METHODS:
            return True
        
        # escrita só admin
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # admin pode tudo
        if request.user.is_staff:
            return True
        
        # dono pode acessar
        return obj.user == request.user