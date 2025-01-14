from rest_framework.permissions import BasePermission


class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.is_staff
