from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
