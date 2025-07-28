from abc import abstractmethod, ABC, ABCMeta
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, BasePermissionMetaclass

from users.models import CustomUser, Permission, PermissionType
from workflows.models import UserRole, Workspace, Workflow


def _get_permission_map(**kwargs):
    return kwargs


class PermissionMixin:

    def get_workspace_from_view(self, view) -> Workspace:
        try:
            ws = view.kwargs.get("workspace_pk") or view.kwargs.get("workspace_id")
            if ws:
                return get_object_or_404(Workspace, pk=ws)

            wf = view.kwargs.get("workflow_pk") or view.kwargs.get("workflow_id")
            if wf:
                workflow = get_object_or_404(Workflow, pk=wf)
                return workflow.workspace
        except Http404:
            raise AttributeError

        raise AttributeError

    def _get_user_permissions(self, user: CustomUser, workspace) -> set:
        if not user.is_authenticated:
            return set()

        try:
            workspace_role = user.user_roles.select_related("role").get(workspace=workspace)
            permissions = Permission.objects.filter(rolepermission__role=workspace_role.role).values_list("name",
                                                                                                          flat=True)
        except UserRole.DoesNotExist:
            return set()

        return set(permissions)

    def user_has_permission(self, user: CustomUser, workspace: Workspace, req_perm: PermissionType) -> bool:
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

    def has_permission(self, request, view, **kwargs):
        user: CustomUser = request.user
        if not user or not user.is_authenticated:
            return False

        # checking if there is workflow passed in kwargs (from WorkflowConfigPermission)
        workflow = kwargs.get("workflow")
        if workflow and isinstance(workflow, Workflow):
            return self._get_final_permission(user, workflow.workspace, view)

        try:
            ws = self.get_workspace_from_view(view)
        except AttributeError:
            return True

        return self._get_final_permission(user, ws, view)

    def has_object_permission(self, request, view, obj):
        user: CustomUser = request.user
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
        if (request.method in ['PUT', 'DELETE']
                and request.user
                and request.user.is_authenticated
                and obj.created_by == request.user):
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

    # allows update, delete by workflow creator
    def has_object_permission(self, request, view, obj):
        if (request.method in ['PUT', 'DELETE']
                and request.user
                and request.user.is_authenticated
                and request.user == obj.workflow.created_by):
            return True

        return super().has_object_permission(request, view, obj)

    # allows creation by workflow creator
    def has_permission(self, request, view, **kwargs):
        if (request.method == 'POST'
                and request.user and request.user.is_authenticated):
            wf = view.kwargs.get("workflow_pk") or view.kwargs.get("workflow_id")
            if wf:
                try:
                    workflow = get_object_or_404(Workflow, pk=wf)
                    if workflow.created_by == request.user:
                        return True
                except Http404:
                    return super().has_permission(request, view)

        return super().has_permission(request, view, workflow=workflow)


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

    # allows retrieval by workflow creator
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
