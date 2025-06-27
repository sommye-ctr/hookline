from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView, Response

from workflows.models import Workspace, Workflow, Trigger, Action, ExecutionLog, WebhookEndpoint, InstalledPlugin
from workflows.serializers import WorkspaceListSerializer, WorkspaceSerializer, WorkflowListSerializer, \
    WorkflowSerializer, TriggerSerializer, ActionSerializer, ExecutionLogSerializer, ExecutionLogListSerializer, \
    WebhookEndpointSerializer, InstalledPluginListSerializer, InstalledPluginSerializer
from .tasks import log_event_task
from .utils import extract_event_type, load_json_file


class WorkspaceView(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkspaceListSerializer
        else:
            return WorkspaceSerializer


class WorkflowView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class WorkspaceWorkflowView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
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
        serializer.save(workspace=workspace)


class TriggerView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer


class WorkflowTriggerView(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = TriggerSerializer

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
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class WorkflowActionView(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = ActionSerializer

    def get_workflow(self):
        return get_object_or_404(Workflow, pk=self.kwargs['workflow_pk'])

    def get_queryset(self):
        workflow = self.get_workflow()
        return Action.objects.filter(workflow=workflow)

    def perform_create(self, serializer):
        workflow = self.get_workflow()
        serializer.save(workflow=workflow)


class ExecutionLogsView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ExecutionLog.objects.all()
    serializer_class = ExecutionLogSerializer


class WorkflowExecutionLogsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ExecutionLogListSerializer

    def get_queryset(self):
        wf = get_object_or_404(Workflow, pk=self.kwargs['workflow_pk'])
        return ExecutionLog.objects.filter(workflow=wf)


class WebhookEndpointView(viewsets.ModelViewSet):
    queryset = WebhookEndpoint.objects.all()
    serializer_class = WebhookEndpointSerializer
    http_method_names = ['get', 'post', 'delete']


class WebhookReceiverView(APIView):
    def post(self, request, token):
        endpoint = get_object_or_404(WebhookEndpoint, token=token)

        event_type = extract_event_type(request.data, endpoint.platform)
        log_event_task(endpoint.workspace_id, request.data, event_type)
        return Response("Received", status=status.HTTP_200_OK)


class PluginsView(APIView):
    def get(self, request):
        try:
            plugins = load_json_file("plugins/register.json")
        except FileNotFoundError:
            return Response("Could not find plugins registry", status=status.HTTP_404_NOT_FOUND)

        return Response(plugins, status=status.HTTP_200_OK)


class InstalledPluginsView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    def get_queryset(self):
        return InstalledPlugin.objects.filter(workspace_id=self.kwargs['workspace_pk'])

    def get_serializer_class(self):
        if self.action == 'list':
            return InstalledPluginListSerializer
        else:
            return InstalledPluginSerializer

    # TODO - Handle the update of plugins
    def create(self, request, *args, **kwargs):
        ws = self.kwargs['workspace_pk']
        slug = request.data['slug']

        try:
            plugins: list = load_json_file("plugins/register.json")
        except FileNotFoundError:
            return Response("There was an error while fetching plugins", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        plugin = [x for x in plugins if x['slug'] == slug]
        if len(plugin) < 1:
            return Response(f"Plugin {slug} not found", status=status.HTTP_404_NOT_FOUND)

        installed = InstalledPlugin.objects.create(workspace_id=ws, **plugin[0])
        obj = InstalledPluginSerializer(installed)
        return Response(obj.data, status=status.HTTP_201_CREATED)
