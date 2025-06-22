from django.urls import path, include
from rest_framework_nested import routers
from workflows import views

router = routers.DefaultRouter()
router.register("workspaces", views.WorkspaceView)
router.register("workflows", views.WorkflowView)

workspace_router = routers.NestedDefaultRouter(router, "workspaces", lookup='workspace')
workspace_router.register("workflows", views.WorkspaceWorkflowView, basename="workspace-workflow")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(workspace_router.urls))
]