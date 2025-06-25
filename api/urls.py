from django.urls import path, include
from rest_framework_nested import routers
from workflows import views

router = routers.DefaultRouter()
router.register("workspaces", views.WorkspaceView)
router.register("workflows", views.WorkflowView)
router.register("triggers", views.TriggerView)
router.register("actions", views.ActionView)
router.register("execution-logs", views.ExecutionLogsView)
router.register("webhook-endpoints", views.WebhookEndpointView)

workspace_router = routers.NestedDefaultRouter(router, "workspaces", lookup='workspace')
workspace_router.register("workflows", views.WorkspaceWorkflowView, basename="workspace-workflow")

workflow_router = routers.NestedDefaultRouter(router, "workflows", lookup="workflow")
workflow_router.register("triggers", views.WorkflowTriggerView, basename="workflow-trigger")
workflow_router.register("actions", views.WorkflowActionView, basename="workflow-action")
workflow_router.register("execution-logs", views.WorkflowExecutionLogsView, basename="workflow-execution-logs")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(workspace_router.urls)),
    path('', include(workflow_router.urls)),
    path('webhooks/<token>/ingest', views.WebhookReceiverView.as_view(), name='webhook-ingest'),
    path('plugins/', views.PluginsView.as_view(), name="plugins")
]
