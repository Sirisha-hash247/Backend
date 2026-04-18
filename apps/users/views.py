from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from core.permissions import IsAdminUserRole

from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer
)

from .services.auth_service import  login_user
from .services.user_service import get_all_users


class RegisterView(APIView):

    @extend_schema(
        request=RegisterSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()   

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    @extend_schema(
        request=LoginSerializer,
        responses={200: dict},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = login_user(
            serializer.validated_data['email'],
            serializer.validated_data['password']
        )

        return Response({
            "user": UserSerializer(data["user"]).data,
            "tokens": data["tokens"]
        })


class UserListView(APIView):
    permission_classes =  [IsAuthenticated, IsAdminUserRole]

    @extend_schema(
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        users = get_all_users()
        return Response(UserSerializer(users, many=True).data)