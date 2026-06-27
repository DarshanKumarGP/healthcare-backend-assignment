from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """POST /api/auth/register/ payload: { name, email, password }"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value.lower()

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Name cannot be empty.')
        return value.strip()

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
        )


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of a user, nested inside the login response."""

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'date_joined')
        read_only_fields = fields


class LoginSerializer(TokenObtainPairSerializer):
    """
    Extends simplejwt's default serializer so the login response
    includes basic user details alongside the access/refresh tokens,
    instead of forcing the client to decode the JWT to know who
    just logged in.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
