from django.urls import path, include
from rest_framework_nested import routers
from workflows import views

router = routers.DefaultRouter()
router.register("workspaces", views.WorkspaceView)
router.register("workflows", views.WorkflowView)
router.register("triggers", views.TriggerView)
router.register("actions", views.ActionView)

workspace_router = routers.NestedDefaultRouter(router, "workspaces", lookup='workspace')
workspace_router.register("workflows", views.WorkspaceWorkflowView, basename="workspace-workflow")

workflow_router = routers.NestedDefaultRouter(router, "workflows", lookup="workflow")
workflow_router.register("triggers", views.WorkflowTriggerView, basename="workflow-trigger")
workflow_router.register("actions", views.WorkflowActionView, basename="workflow-action")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(workspace_router.urls)),
    path('', include(workflow_router.urls))
]