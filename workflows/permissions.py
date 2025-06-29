from enum import Enum

from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission

from workflows.models import PermissionType


class RoleType(Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class RoleBasedPermission(BasePermission):
    def __init__(self, req_perm=None, req_role=None):
        self.req_perm = req_perm
        self.req_role = req_role

    def has_permission(self, request, view):
        user: User = request.user
        if not user.is_authenticated:
            return False

        ws = getattr(request, 'workspace', None)
        if not ws:
            return False

        user_roles = user.user_roles.filter(workspace=ws, user=user)

        for u in user_roles:
            if self.req_role:
                return u.role.name == self.req_role
            elif self.req_perm:
                return self.req_perm in u.role.permissions.all()

        return False


class RequireRole(RoleBasedPermission):
    def __init__(self, role: RoleType):
        super().__init__(req_role=role.name)


class RequirePermission(RoleBasedPermission):
    def __init__(self, permission: PermissionType):
        super().__init__(req_perm=permission.name)
