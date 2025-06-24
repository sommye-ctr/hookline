from django.shortcuts import get_object_or_404

from .models import Workflow, Trigger, Workspace

def get_nested_value(data: dict, dotted_path: str, default=None):
    keys = dotted_path.split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data

class TrelloCardCreatedMatcher:
    def __init__(self, event_payload, workspace_id):
        self.event_payload = event_payload
        self.workspace_id = workspace_id
        self.event_type = event_payload['action']['type'] #gives createCard

    def match(self):
        ws = get_object_or_404(Workspace, pk=self.workspace_id)
        for wf in ws.workflows:
            if not wf.is_active:
                break
            for tr in wf.triggers:
                if tr.type == self.event_type:
                    for obj in self.event_payload:
                        value = get_nested_value(self.event_payload, obj['field'])
                        if value == obj['equals']:
                            return tr.id
                        else:
                            break
        return -1
