from enum import Enum

from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission


class PermissionType(Enum):
    READ_WORKSPACE = "read_workspace"  # include both list and retrieve
    UPDATE_WORKSPACE = "update_workspace"
    DELETE_WORKSPACE = "delete_workspace"

    READ_WORKFLOW = "read_workflow"
    UPDATE_WORKFLOW = "update_workflow"
    DELETE_WORKFLOW = "delete_workflow"
    CREATE_WORKFLOW = "create_workflow"

    READ_TRIGGER = "read_trigger"
    UPDATE_TRIGGER = "update_trigger"
    DELETE_TRIGGER = "delete_trigger"
    CREATE_TRIGGER = "create_trigger"

    READ_ACTION = "read_action"
    UPDATE_ACTION = "update_action"
    DELETE_ACTION = "delete_action"
    CREATE_ACTION = "create_action"

    READ_EX_LOGS = "read_ex_logs"

    READ_WEBHOOK_ENDPOINTS = "read_webhook_endpoints"
    WRITE_WEBHOOK_ENDPOINTS = "write_webook_endpoints"

    READ_INSTALLED_PLUGINS = "read_installed_plugins"
    UPDATE_INSTALLED_PLUGINS = "update_installed_plugins"
    DELETE_INSTALLED_PLUGINS = "delete_installed_plugins"
    CREATE_INSTALLED_PLUGINS = "create_installed_plugins"


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
