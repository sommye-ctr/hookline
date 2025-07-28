from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class PermissionType(models.TextChoices):
    READ_WORKSPACE = "read_workspace", "Read Workspace"
    UPDATE_WORKSPACE = "update_workspace", "Update Workspace"
    DELETE_WORKSPACE = "delete_workspace", "Delete Workspace"

    READ_WORKFLOW = "read_workflow", "Read Workflow"
    UPDATE_WORKFLOW = "update_workflow", "Update Workflow"
    DELETE_WORKFLOW = "delete_workflow", "Delete Workflow"
    CREATE_WORKFLOW = "create_workflow", "Create Workflow"

    READ_WF_CONFIG = "read_wf_config", "Read trigger/action of workflow"
    UPDATE_WF_CONFIG = "update_wf_config", "Update trigger/action of workflow"
    DELETE_WF_CONFIG = "delete_wf_config", "Delete trigger/action of workflow"
    CREATE_WF_CONFIG = "create_wf_config", "Create trigger/action of workflow"

    READ_EX_LOGS = "read_ex_logs", "Read Execution Logs"

    READ_WEBHOOK_ENDPOINTS = "read_webhook_endpoints", "Read Webhook Endpoints"
    WRITE_WEBHOOK_ENDPOINTS = "write_webhook_endpoints", "Write Webhook Endpoints"

    READ_INSTALLED_PLUGINS = "read_installed_plugins", "Read Installed Plugins"
    UPDATE_INSTALLED_PLUGINS = "update_installed_plugins", "Update Installed Plugins"
    DELETE_INSTALLED_PLUGINS = "delete_installed_plugins", "Delete Installed Plugins"
    CREATE_INSTALLED_PLUGINS = "create_installed_plugins", "Create Installed Plugins"


class RoleType(models.TextChoices):
    ADMIN = "admin", "ADMIN"
    MEMBER = "member", "MEMBER"


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Permission(models.Model):
    name = models.CharField(max_length=100, choices=PermissionType, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()


# admin, member
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True, choices=RoleType)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, related_name="permissions")
    permission = models.ForeignKey(to=Permission, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} with {self.permission.name}"
