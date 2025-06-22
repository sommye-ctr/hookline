from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from workflows.models import Workspace, Workflow, Trigger, Action
from workflows.serializers import WorkspaceListSerializer, WorkspaceSerializer, WorkflowListSerializer, \
    WorkflowSerializer, TriggerSerializer, ActionSerializer


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