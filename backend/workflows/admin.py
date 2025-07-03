from django.contrib import admin

from workflows.models import Workspace, Workflow, Trigger, Action, ExecutionLog, WebhookEndpoint, InstalledPlugin, \
    Permission, Role

admin.site.register(Workspace)
admin.site.register(Workflow)
admin.site.register(Trigger)
admin.site.register(Action)
admin.site.register(ExecutionLog)
admin.site.register(WebhookEndpoint)
admin.site.register(InstalledPlugin)
admin.site.register(Permission)
admin.site.register(Role)
