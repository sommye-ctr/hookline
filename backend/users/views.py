from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


# Create your views here.
class SignupView(APIView):
    def post(self, request):
        permission_classes = [AllowAny]

