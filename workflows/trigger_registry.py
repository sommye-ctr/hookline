from django.shortcuts import get_object_or_404

from .models import Workspace
from .utils import get_nested_value


class TriggerMatcher:
    def __init__(self, payload, workspace_id, event_type):
        self.payload = payload
        self.workspace_id = workspace_id
        self.event_type = event_type

    def match(self):
        ws = get_object_or_404(Workspace, pk=self.workspace_id)

        for wf in ws.workflows.all():
            if not wf.is_active:
                break
            for tr in wf.triggers.all():
                if tr.type == self.event_type:
                    for obj in tr.config:
                        value = get_nested_value(self.payload, obj['field'])
                        if value == obj['value']:
                            return wf.id, tr.id
                        else:
                            break
        return None
