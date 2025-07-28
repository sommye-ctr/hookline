from rest_framework import serializers
from packaging.version import parse as parse_version

from users.models import CustomUser
from users.serializers import UserSerializer
from workflows.models import Workspace, Trigger, Action, Workflow, ExecutionLog, WebhookEndpoint, InstalledPlugin

from json import JSONEncoder
from uuid import UUID

old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default


class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source="owner",
        write_only=True
    )
    workflows_count = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owner', 'owner_id', 'workflows_count', 'date_created', 'date_updated']
        read_only_fields = ['id', 'date_updated', 'date_created']

    def get_workflows_count(self, workspace):
        return workspace.workflows.count()


class WorkspaceListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    workflows_count = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owner', 'workflows_count', 'date_created']
        read_only_fields = ['id', 'date_created']

    def get_workflows_count(self, obj):
        return obj.workflows.count()


class TriggerSerializer(serializers.ModelSerializer):
    id = str()

    class Meta:
        model = Trigger
        fields = "__all__"

    def validate_config(self, config):
        if not isinstance(config, list):
            raise serializers.ValidationError("Config must be list of json objects")

        for item in config:
            if not isinstance(item, dict):
                raise serializers.ValidationError("Config item must be a valid json object")
            if not any(hasattr(item, attr) for attr in ['field', 'value']):
                raise serializers.ValidationError("Config item must have field & value attribute")


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"

    def validate_order(self, value):
        if value < 1:
            raise serializers.ValidationError("Order must be greater than 0")
        return value


class WorkflowListSerializer(serializers.ModelSerializer):
    workspace_name = serializers.CharField(source='workspace.name', read_only=True)
    triggers_count = serializers.SerializerMethodField()
    actions_count = serializers.SerializerMethodField()

    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'is_active', 'workspace_name',
            'triggers_count', 'actions_count', 'date_created', 'date_updated', 'created_by_id'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

    def get_triggers_count(self, obj):
        return obj.triggers.count()

    def get_actions_count(self, obj):
        return obj.actions.count()


class WorkflowSerializer(serializers.ModelSerializer):
    workspace = WorkspaceListSerializer(read_only=True)
    # workspace_id = serializers.UUIDField(write_only=True)
    triggers = TriggerSerializer(many=True, read_only=True)
    actions = ActionSerializer(many=True, read_only=True)
    recent_logs = serializers.SerializerMethodField()

    class Meta:
        model = Workflow
        fields = [
            'id', 'name', 'description', 'is_active', 'workspace',
            'triggers', 'actions', 'recent_logs',
            'date_created', 'date_updated', 'created_by'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

    def get_recent_logs(self, obj):
        recent_logs = obj.logs.order_by('-timestamp')[:10]
        return ExecutionLogSerializer(recent_logs, many=True).data


class ExecutionLogSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source='workflow.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ExecutionLog
        fields = [
            'id', 'workflow', 'workflow_name', 'timestamp',
            'status', 'status_display', 'details'
        ]
        read_only_fields = ['id', 'timestamp']


class ExecutionLogListSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source='workflow.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ExecutionLog
        fields = [
            'id', 'workflow', 'workflow_name', 'timestamp', 'status', 'status_display'
        ]
        read_only_fields = ['id', 'timestamp']


class WebhookEndpointSerializer(serializers.ModelSerializer):
    workspace = WorkspaceListSerializer(read_only=True)
    workspace_id = serializers.PrimaryKeyRelatedField(
        queryset=Workspace.objects.all(),
        source="workspace",
        write_only=True
    )

    # TODO - Look for token encryption
    class Meta:
        model = WebhookEndpoint
        fields = ['workspace', 'workspace_id', 'platform', 'token', 'date_created']


class InstalledPluginListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstalledPlugin
        fields = ["id", "slug", "name", "version", "icon"]


class InstalledPluginSerializer(serializers.ModelSerializer):
    installed_by = UserSerializer(read_only=True)
    name = serializers.CharField(read_only=True)
    version = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)
    icon = serializers.CharField(read_only=True)
    user_config = serializers.JSONField(read_only=True)

    class Meta:
        model = InstalledPlugin
        fields = ["slug", "name", "version", "icon", "version", "description",
                  "author", "user_config", "installed_by"]

    def validate_version(self, obj):
        parse_version(obj)
        return obj
