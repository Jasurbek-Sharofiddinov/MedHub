from rest_framework import permissions

from doctors.models import MedicalProfessional


class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and MedicalProfessional.objects.filter(user__id=request.user.id).exists()
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser or request.method in permissions.SAFE_METHODS
