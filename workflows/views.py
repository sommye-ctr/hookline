from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, mixins
from workflows.models import Workspace, Workflow
from workflows.serializers import WorkspaceListSerializer, WorkspaceSerializer, WorkflowListSerializer, \
    WorkflowSerializer


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
