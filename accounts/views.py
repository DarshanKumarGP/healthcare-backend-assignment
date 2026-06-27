from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView

from core.utils import success_response

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ -- Register a new user with name, email, and password."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(
            data={'id': user.id, 'name': user.name, 'email': user.email},
            message='User registered successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """POST /api/auth/login/ -- Authenticate a user and return a JWT token pair."""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(
            data=serializer.validated_data,
            message='Login successful.',
            status_code=status.HTTP_200_OK,
        )
