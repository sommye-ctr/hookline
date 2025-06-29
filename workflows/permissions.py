from abc import abstractmethod, ABC, ABCMeta
from enum import Enum

from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, BasePermissionMetaclass

from workflows.models import PermissionType, Permission, UserRole, Workspace, Workflow, Trigger


class RoleType(Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


def _get_permission_map(**kwargs):
    return kwargs


class PermissionMixin:

    # TODO Implement workspace object retrieval
    def get_workspace_from_view(self, request, view) -> Workspace:
        raise AttributeError

    def _get_user_permissions(self, user: User, workspace) -> set:
        if not user.is_authenticated:
            return set()

        try:
            workspace_role = user.user_roles.select_related("role").get(workspace=workspace)
            permissions = Permission.objects.filter(rolepermission__role=workspace_role.role).values_list("name",
                                                                                                          flat=True)
        except UserRole.DoesNotExist:
            return set()

        return set(permissions)

    def user_has_permission(self, user: User, workspace: Workspace, req_perm: PermissionType) -> bool:
        if not user.is_authenticated:
            return False

        permissions = self._get_user_permissions(user, workspace)
        return req_perm in permissions


class HooklineMetaClass(BasePermissionMetaclass, ABCMeta):
    pass


class HooklinePermission(BasePermission, ABC, PermissionMixin, metaclass=HooklineMetaClass):
    @property
    @abstractmethod
    def permission_map(self) -> dict[str: PermissionType]:
        pass

    @abstractmethod
    def get_workspace_from_obj(self, obj) -> Workspace:
        pass

    def _get_final_permission(self, user, ws, view):
        required_perm: PermissionType = self.permission_map.get(view.action)
        if not required_perm:
            return True
        return self.user_has_permission(user, ws, required_perm)

    def has_permission(self, request, view):
        user: User = request.user
        if not user or not user.is_authenticated:
            return False

        try:
            ws = self.get_workspace_from_view(request, view)
        except AttributeError:
            return True

        return self._get_final_permission(user, ws, view)

    def has_object_permission(self, request, view, obj):
        user: User = request.user
        if not user or not user.is_authenticated:
            return False

        try:
            ws = self.get_workspace_from_obj(obj)
        except AttributeError:
            return False

        return self._get_final_permission(user, ws, view)


class WorkspacePermission(HooklinePermission):
    permission_map = _get_permission_map(
        list=PermissionType.READ_WORKSPACE,
        retrieve=PermissionType.READ_WORKSPACE,
        update=PermissionType.UPDATE_WORKSPACE,
        delete=PermissionType.DELETE_WORKSPACE,
    )

    def get_workspace_from_obj(self, obj) -> Workspace:
        return obj


class WorkflowPermission(HooklinePermission):
    permission_map = _get_permission_map(
        list=PermissionType.READ_WORKFLOW,
        retrieve=PermissionType.READ_WORKFLOW,
        update=PermissionType.UPDATE_WORKFLOW,
        delete=PermissionType.DELETE_WORKFLOW,
        create=PermissionType.CREATE_WORKFLOW,
    )

    def get_workspace_from_obj(self, obj) -> Workspace:
        return obj.workspace

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE'] and request.user and obj.created_by == request.user:
            return True

        return super().has_object_permission(request, view, obj)


class WorkflowConfigPermission(HooklinePermission):
    permission_map = _get_permission_map(
        list=PermissionType.READ_WF_CONFIG,
        retrieve=PermissionType.READ_WF_CONFIG,
        update=PermissionType.UPDATE_WF_CONFIG,
        delete=PermissionType.DELETE_WF_CONFIG,
        create=PermissionType.CREATE_WF_CONFIG,
    )

    def get_workspace_from_obj(self, obj) -> Workspace:
        return obj.workflow.workspace

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE'] and request.user and request.user == obj.workflow.created_by:
            return True

        return super().has_object_permission(request, view, obj)


class WebhookEndpointPermission(HooklinePermission):
    permission_map = _get_permission_map(
        list=PermissionType.READ_WEBHOOK_ENDPOINTS,
        retrieve=PermissionType.READ_WEBHOOK_ENDPOINTS,
        update=PermissionType.WRITE_WEBHOOK_ENDPOINTS,
        delete=PermissionType.WRITE_WEBHOOK_ENDPOINTS,
        create=PermissionType.WRITE_WEBHOOK_ENDPOINTS,
    )

    def get_workspace_from_obj(self, obj) -> Workspace:
        return obj.workspace


class ExecutionLogPermission(HooklinePermission):
    permission_map = _get_permission_map(
        list=PermissionType.READ_EX_LOGS,
    )

    def get_workspace_from_obj(self, obj) -> Workspace:
        return obj.workflow.workspace

    def has_object_permission(self, request, view, obj):
        if request.user and request.user == obj.workflow.created_by:
            return True

        return super().has_object_permission(request, view, obj)


class InstalledPluginPermission(HooklinePermission):
    permission_map = _get_permission_map(
        list=PermissionType.READ_INSTALLED_PLUGINS,
        retrieve=PermissionType.READ_INSTALLED_PLUGINS,
        update=PermissionType.UPDATE_INSTALLED_PLUGINS,
        delete=PermissionType.DELETE_INSTALLED_PLUGINS,
        create=PermissionType.CREATE_INSTALLED_PLUGINS,
    )

    def get_workspace_from_obj(self, obj) -> Workspace:
        return obj.workspace
