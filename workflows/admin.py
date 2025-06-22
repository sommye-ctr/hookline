from django.contrib import admin

from workflows.models import Workspace, Workflow, Trigger, Action, ExecutionLog

admin.site.register(Workspace)
admin.site.register(Workflow)
admin.site.register(Trigger)
admin.site.register(Action)
admin.site.register(ExecutionLog)
