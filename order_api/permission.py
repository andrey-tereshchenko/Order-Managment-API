from django.contrib.auth.models import Group
from rest_framework import permissions


def _is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(
            id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    if required_groups:
        return any(
            [_is_in_group(user, group_name) for group_name in required_groups])
    else:
        return False


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    required_groups = ['admin']

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user,
                                                     self.required_groups)
        return obj == request.user or has_group_permission


class IsAdminUser(permissions.BasePermission):
    required_groups = ['admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user,
                                                     self.required_groups)
        return request.user and has_group_permission


class IsAdminOrCashier(permissions.BasePermission):
    required_groups = ['cashier', 'admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user,
                                                     self.required_groups)
        return request.user and has_group_permission


class IsAdminOrCashierOrSeller(permissions.BasePermission):
    required_groups = ['cashier', 'admin', 'seller']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user,
                                                     self.required_groups)
        return request.user and has_group_permission
