import uuid

from django.contrib.auth.models import User
from django.db import models

from workflows.utils import generate_webhook_token


class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="workspaces")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Workflow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    workspace = models.ForeignKey(to=Workspace, on_delete=models.CASCADE, related_name="workflows")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Trigger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(to=Workflow, on_delete=models.CASCADE, related_name="triggers")
    type = models.CharField(max_length=255)
    config = models.JSONField()

    def __str__(self):
        return self.type

class Action(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(to=Workflow, on_delete=models.CASCADE, related_name="actions")
    type = models.CharField(max_length=255)
    config = models.JSONField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.type

class ExecutionLog(models.Model):
    TRIGGER_MATCHED = "TM"
    ACTION_ENQUEUED = "AE"
    ACTION_STARTED = "AS"
    ACTION_COMPLETED = "AC"
    ACTION_FAILED = "AF"
    RETRY_SCHEDULED = "RS"
    RETRY_FAILED = "RF"
    INTERNAL_ERROR = "IE"
    PLUGIN_PROTOCOL_ERROR = "PP"

    STATUS_CHOICES = [
        (TRIGGER_MATCHED, 'Trigger matched'),
        (ACTION_ENQUEUED, 'Action enqueued'),
        (ACTION_STARTED, 'Action execution started'),
        (ACTION_COMPLETED, 'Action completed'),
        (ACTION_FAILED, 'Action failed'),
        (RETRY_SCHEDULED, 'Retry scheduled'),
        (RETRY_FAILED, 'Retry failed'),
        (INTERNAL_ERROR, 'Internal error'),
        (PLUGIN_PROTOCOL_ERROR, "Plugin Protocol error"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(to=Workflow, on_delete=models.CASCADE, related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    details = models.JSONField(default=dict)

    def __str__(self):
        return self.status

    @staticmethod
    def log_entry(workflow_id:uuid.UUID, status, detail:dict):
        ExecutionLog.objects.create(
            workflow_id=workflow_id,
            status=status,
            details=detail
        )


class WebhookEndpoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(to=Workspace, on_delete=models.CASCADE, related_name="webhooks")
    platform = models.CharField(max_length=64)
    token = models.CharField(max_length=64, unique=True, default=generate_webhook_token, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("workspace", "platform")


class InstalledPlugin(models.Model):
    workspace = models.ForeignKey(to=Workspace, on_delete=models.CASCADE, related_name="installed_plugins", editable=False)
    slug = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=20)
    description = models.TextField()
    author = models.CharField(max_length=200)
    icon = models.TextField()
    config_schema = models.JSONField()
    user_config = models.JSONField() #TODO - db validator to prevent incorrect config
    installed_at = models.DateTimeField(auto_now_add=True, editable=False)
    installed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    class Meta:
        unique_together = ('workspace', 'slug')
