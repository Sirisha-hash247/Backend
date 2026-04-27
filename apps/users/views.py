from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from drf_spectacular.utils import extend_schema

from core.permissions import IsAdminUserRole, IsSuperAdmin, IsAdminOrSuperAdmin
from core.roles import Roles

from apps.users.models import User, Organization   # ✅ FIXED IMPORT
from apps.users.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    OrganizationSerializer
)

from apps.users.services.auth_service import login_user
from apps.users.services.user_service import get_all_users
 


# ---------------- AUTH ---------------- #

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
        
        
# Paste this AFTER the LoginView class in apps/users/views.py

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "organization_id": str(user.organization.id) if user.organization else None,
        })


# ---------------- USERS ---------------- #

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    # GET (LIST USERS)
    def get(self, request):
        users = get_all_users(request.user)
        return Response(UserSerializer(users, many=True).data)

    # CREATE USER
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 🔒 ADMIN → only inside their org
        if request.user.role != Roles.SUPER_ADMIN:
            serializer.save(organization=request.user.organization)
        else:
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # UPDATE USER
    def patch(self, request, user_id):
        try:
            if request.user.role == Roles.SUPER_ADMIN:
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.get(
                    id=user_id,
                    organization=request.user.organization
                )
        except User.DoesNotExist:
            raise ValidationError("User not found")

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    # DELETE USER
    def delete(self, request, user_id):
        try:
            if request.user.role == Roles.SUPER_ADMIN:
                user = User.objects.get(id=user_id)
            else:
                user = User.objects.get(
                    id=user_id,
                    organization=request.user.organization
                )
        except User.DoesNotExist:
            raise ValidationError("User not found")

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- ORGANIZATION ---------------- #

# apps/users/views.py

from rest_framework.exceptions import ValidationError


class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        return Organization.objects.all()

    def perform_create(self, serializer):
        admin_user_id = serializer.validated_data.pop("admin_user")

        org = serializer.save()

        try:
            user = User.objects.get(id=admin_user_id)
        except User.DoesNotExist:
            raise ValidationError("Invalid admin_user")

        if user.organization:
            raise ValidationError("User already belongs to another organization")

        user.organization = org
        user.role = "admin"
        user.save()


class OrganizationUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def get(self, request, org_id):
        users = User.objects.filter(organization_id=org_id)
        return Response(UserSerializer(users, many=True).data)
    
