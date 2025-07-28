from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import views

urlpatterns = [
    path('signup/', views.SignupView),
    path('token', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
