from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from workflows import views

router = routers.DefaultRouter()
router.register("workspaces", views.WorkspaceView, basename="workspace")
router.register("workflows", views.WorkflowView, basename="workflow")
router.register("triggers", views.TriggerView, basename="trigger")
router.register("actions", views.ActionView, basename="action")

workspace_router = routers.NestedDefaultRouter(router, "workspaces", lookup='workspace')
workspace_router.register("workflows", views.WorkspaceWorkflowView, basename="workspace-workflow")
workspace_router.register("installed-plugins", views.InstalledPluginsView, basename="installed-plugins")
workspace_router.register("webhook-endpoints", views.WebhookEndpointView, basename="webhook-endpoints")

workflow_router = routers.NestedDefaultRouter(router, "workflows", lookup="workflow")
workflow_router.register("triggers", views.WorkflowTriggerView, basename="workflow-trigger")
workflow_router.register("actions", views.WorkflowActionView, basename="workflow-action")
workflow_router.register("execution-logs", views.WorkflowExecutionLogsView, basename="workflow-execution-logs")

user_router =routers.NestedDefaultRouter(router, "user", lookup="user")
user_router.register('token', TokenObtainPairView.as_view(), basename='token-obtain-pair')
user_router.register('refresh/', TokenRefreshView.as_view(), basename='token-refresh')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(workspace_router.urls)),
    path('', include(workflow_router.urls)),
    path('webhooks/<token>/ingest', views.WebhookReceiverView.as_view(), name='webhook-ingest'),
    path('plugins/', views.PluginsView.as_view(), name="plugins"),
    path('user/', include('users.urls'))
]
