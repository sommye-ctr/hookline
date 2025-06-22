from rest_framework import viewsets

from workflows.models import Workspace
from workflows.serializers import WorkspaceListSerializer, WorkspaceSerializer


class WorkspaceView(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkspaceListSerializer
        else:
            return WorkspaceSerializer

