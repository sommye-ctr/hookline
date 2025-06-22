from django.urls import path, include
from rest_framework.routers import DefaultRouter
from workflows import views

router = DefaultRouter()
router.register("workspaces", views.WorkspaceView)

urlpatterns = [
    path('', include(router.urls))
]