from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from packaging.version import parse as parse_version, InvalidVersion

from workflows.models import Workspace, Workflow, Trigger, Action, ExecutionLog, WebhookEndpoint, InstalledPlugin
from workflows.serializers import WorkspaceListSerializer, WorkspaceSerializer, WorkflowListSerializer, \
    WorkflowSerializer, TriggerSerializer, ActionSerializer, ExecutionLogListSerializer, \
    WebhookEndpointSerializer, InstalledPluginListSerializer, InstalledPluginSerializer
from users.permissions import WorkspacePermission, WebhookEndpointPermission, ExecutionLogPermission, \
    InstalledPluginPermission, WorkflowPermission, WorkflowConfigPermission
from .tasks import log_event_task
from .utils import extract_event_type, load_json_file


class WorkspaceView(viewsets.ModelViewSet):
    permission_classes = [WorkspacePermission]

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkspaceListSerializer
        else:
            return WorkspaceSerializer

    def get_queryset(self):
        return Workflow.objects.filter(workspace__members=self.request.user)


class WorkflowView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = WorkflowSerializer
    permission_classes = [WorkflowPermission]

    def get_queryset(self):
        return Workflow.objects.filter(workspace__members=self.request.user)


class WorkspaceWorkflowView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [WorkflowPermission]

    def get_queryset(self):
        workspace = get_object_or_404(Workspace, pk=self.kwargs['workspace_pk'])
        return Workflow.objects.filter(workspace=workspace)

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkflowListSerializer
        else:
            return WorkflowSerializer

    def perform_create(self, serializer):
        workspace = get_object_or_404(Workspace, pk=self.kwargs['workspace_pk'])
        creator = self.request.user
        serializer.save(workspace=workspace, created_by=creator)


class TriggerView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TriggerSerializer
    permission_classes = [WorkflowConfigPermission]

    def get_queryset(self):
        return Trigger.objects.filter(workflow__workspace__members=self.request.user)


class WorkflowTriggerView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = TriggerSerializer
    permission_classes = [WorkflowConfigPermission]

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['workflow_pk'])

    def get_queryset(self):
        workflow = self.get_workflow()
        return Trigger.objects.filter(workflow=workflow)

    def perform_create(self, serializer):
        workflow = self.get_workflow()
        serializer.save(workflow=workflow)


class ActionView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = ActionSerializer
    permission_classes = [WorkflowConfigPermission]

    def get_queryset(self):
        return Action.objects.filter(workflow__workspace__members=self.request.user)


class WorkflowActionView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ActionSerializer
    permission_classes = [WorkflowConfigPermission]

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['workflow_pk'])

    def get_queryset(self):
        workflow = self.get_workflow()
        return Action.objects.filter(workflow=workflow)

    def perform_create(self, serializer):
        workflow = self.get_workflow()
        serializer.save(workflow=workflow)


class WorkflowExecutionLogsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExecutionLogListSerializer
    permission_classes = [ExecutionLogPermission]

    def get_queryset(self):
        return ExecutionLog.objects.filter(
            workflow_id=self.kwargs['workflow_pk'],
            workflow__workspace__members=self.request.user
        )


class WebhookEndpointView(viewsets.ModelViewSet):
    serializer_class = WebhookEndpointSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [WebhookEndpointPermission]

    def get_queryset(self):
        return WebhookEndpoint.objects.filter(workspace__members=self.request.user)


class WebhookReceiverView(APIView):
    def post(self, request, token):
        endpoint = get_object_or_404(WebhookEndpoint, token=token)

        event_type = extract_event_type(request.data, endpoint.platform)
        log_event_task(endpoint.workspace_id, request.data, event_type)
        return Response("Received", status=status.HTTP_200_OK)


class PluginsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            plugins = load_json_file("plugins/register.json")
        except FileNotFoundError:
            return Response("Could not find plugins registry", status=status.HTTP_404_NOT_FOUND)

        return Response(plugins, status=status.HTTP_200_OK)


# TODO - use slug instead of id in endpoint
class InstalledPluginsView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [InstalledPluginPermission]

    def get_queryset(self):
        return InstalledPlugin.objects.filter(
            workspace_id=self.kwargs['workspace_pk'],
            workspace__members=self.request.user,
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return InstalledPluginListSerializer
        else:
            return InstalledPluginSerializer

    def _get_plugin(self, slug: str):
        try:
            plugins = load_json_file("plugins/register.json")
        except FileNotFoundError:
            return Response("There was an error while fetching plugins", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        plugin = [x for x in plugins if x['slug'] == slug]
        if len(plugin) < 1:
            return Response(f"Plugin {slug} not found", status=status.HTTP_404_NOT_FOUND)
        return plugin[0]

    def create(self, request, *args, **kwargs):
        ws = self.kwargs['workspace_pk']
        slug = request.data['slug']

        plugin = self._get_plugin(slug)
        installed = InstalledPlugin.objects.create(workspace_id=ws, **plugin)
        obj = InstalledPluginSerializer(installed)
        return Response(obj.data, status=status.HTTP_201_CREATED)

    @action(methods=['put'], detail=True, url_path="update")
    def update_plugin(self, request, *args, **kwargs):
        slug = request.data.get("slug")
        if not slug:
            return Response("Slug is a required field", status=status.HTTP_400_BAD_REQUEST)

        instance: InstalledPlugin = self.get_object()
        plugin = self._get_plugin(slug)

        try:
            installed_ver = parse_version(instance.version)
            current_ver = parse_version(plugin['version'])
        except InvalidVersion:
            return Response(f"There was an error with the versioning of the plugin",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if installed_ver < current_ver:
            instance.version = plugin['version']
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_304_NOT_MODIFIED)
