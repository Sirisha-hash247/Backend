# apps/project/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TestCase
from django_q.tasks import async_task

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .serializers import BulkTestCaseSerializer
from django_q.tasks import async_task



from django.utils import timezone

from .pagination import CustomPagination

from core.permissions import (
    IsAdminOrSuperAdmin,
    IsAdminOrTester,
    IsAdminTesterOrReviewer,
    IsTester,
    IsReviewer,
)

from .models import Project, Module, Screen, TestCase, Bug, TestRun, TestRunVersion
from .serializers import (
    ProjectSerializer, ModuleSerializer, ScreenSerializer,
    TestCaseSerializer, BugSerializer, TestRunSerializer, TestRunVersionSerializer
)
from .services.project_service import create_project, get_all_projects, update_project, delete_project
from .services.module_service import ModuleService
from .services.screen_service import ScreenService
from .services.testcase_service import create_testcase
from .services.bugs_service import create_bug
from .services.testrun_service import TestRunService
from .services.testrun_version_service import TestRunVersionService


from drf_spectacular.utils import extend_schema
from .serializers import BulkTestCaseSerializer


# ─────────────────────────────────────────────
# HELPER — org-scoped queryset filter
# ─────────────────────────────────────────────
def org_filter(qs, user):
    """Filter queryset to the user's organization only."""
    if user.role == "superadmin":
        return qs
    return qs.filter(project__organization=user.organization)


# ─────────────────────────────────────────────
# PROJECT  —  Admin/SuperAdmin only
# ─────────────────────────────────────────────
class ProjectViewSet(ModelViewSet):
    lookup_field = "uuid"
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        else:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Project.objects.none()

        if user.role == "superadmin":
            return Project.objects.filter(deleted_at__isnull=True)

        return Project.objects.filter(
            organization=user.organization,
            deleted_at__isnull=True
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = create_project(request.user, serializer.validated_data)
        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        project = update_project(project, request.user, serializer.validated_data)
        return Response(ProjectSerializer(project).data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        delete_project(project, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────
# MODULE
# ─────────────────────────────────────────────
class ModuleViewSet(ModelViewSet):

    lookup_field = "uuid"

    serializer_class = ModuleSerializer

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:

            return [
                IsAuthenticated(),
                IsAdminTesterOrReviewer()
            ]

        elif self.action == 'destroy':

            return [
                IsAuthenticated(),
                IsAdminOrSuperAdmin()
            ]

        else:

            return [
                IsAuthenticated(),
                IsAdminOrTester()
            ]

    def get_queryset(self):

        user = self.request.user

        if not user.is_authenticated:

            return Module.objects.none()

        queryset = Module.objects.filter(
            deleted_at__isnull=True
        )

        # Organization filter

        if user.role != "superadmin":

            queryset = queryset.filter(
                project__organization=user.organization
            )

        # Project filter

        project_id = self.request.query_params.get(
            "project"
        )

        if project_id:

            queryset = queryset.filter(
                project__uuid=project_id
            )

        return queryset.order_by("name")

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        module = ModuleService.create_module(
            request.user,
            serializer.validated_data
        )

        return Response(

            ModuleSerializer(module).data,

            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        module = self.get_object()

        serializer = self.get_serializer(

            module,

            data=request.data,

            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_module = (
            ModuleService.update_module(
                module,
                request.user,
                serializer.validated_data
            )
        )

        return Response(
            ModuleSerializer(updated_module).data
        )

    def destroy(self, request, *args, **kwargs):

        module = self.get_object()

        ModuleService.delete_module(
            module
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ─────────────────────────────────────────────
# SCREEN
# ─────────────────────────────────────────────
class ScreenViewSet(ModelViewSet):

    lookup_field = "uuid"

    serializer_class = ScreenSerializer

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:

            return [
                IsAuthenticated(),
                IsAdminTesterOrReviewer()
            ]

        elif self.action == 'destroy':

            return [
                IsAuthenticated(),
                IsAdminOrSuperAdmin()
            ]

        else:

            return [
                IsAuthenticated(),
                IsAdminOrTester()
            ]

    def get_queryset(self):

        user = self.request.user

        if not user.is_authenticated:

            return Screen.objects.none()

        queryset = Screen.objects.filter(
            deleted_at__isnull=True
        )

        # Organization filter

        if user.role != "superadmin":

            queryset = queryset.filter(
                module__project__organization=user.organization
            )

        # Module filter

        module_id = self.request.query_params.get(
            "module"
        )

        if module_id:

            queryset = queryset.filter(
                module__uuid=module_id
            )

        return queryset.order_by("name")

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        screen = ScreenService.create_screen(
            request.user,
            serializer.validated_data
        )

        return Response(

            ScreenSerializer(screen).data,

            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        screen = self.get_object()

        serializer = self.get_serializer(

            screen,

            data=request.data,

            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_screen = (
            ScreenService.update_screen(
                screen,
                request.user,
                serializer.validated_data
            )
        )

        return Response(
            ScreenSerializer(updated_screen).data
        )

    def destroy(self, request, *args, **kwargs):

        screen = self.get_object()

        ScreenService.delete_screen(
            screen
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ─────────────────────────────────────────────
# TEST CASE  —  Admin + Tester: CRU  |  Reviewer: R
# ─────────────────────────────────────────────

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import TestCase
from .serializers import TestCaseSerializer
from .pagination import CustomPagination



    


class TestCaseViewSet(ModelViewSet):

    queryset = TestCase.objects.all().order_by("-created_at")

    serializer_class = TestCaseSerializer

    pagination_class = CustomPagination

    filter_backends = [SearchFilter]

    search_fields = [
        "title",
        "description"
    ]

    lookup_field = "uuid"

    def get_queryset(self):

        queryset = super().get_queryset()

        screen = self.request.query_params.get(
            "screen"
        )

        if screen:

            queryset = queryset.filter(
                screen=screen
            )

        return queryset

# ─────────────────────────────────────────────
# TEST RUN  —  Admin + Tester: CRU  |  Reviewer: R + comment patch
# ─────────────────────────────────────────────
class TestRunViewSet(ModelViewSet):

    lookup_field = "uuid"

    serializer_class = TestRunSerializer

    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=["get"],
        url_path="by-version/(?P<version_id>[^/.]+)"
    )
    def by_version(self, request, version_id=None):

        queryset = TestRunService.get_by_version(
            version_id
        )

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:

            serializer = self.get_serializer(
                page,
                many=True
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(
            queryset,
            many=True
        )

        return Response(serializer.data)

# ─────────────────────────────────────────────
# BUG  —  Admin + Tester: CRUD  |  Reviewer: R + comment patch
# ─────────────────────────────────────────────

    
    
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Bug
from .serializers import BugSerializer
from .pagination import CustomPagination


class BugViewSet(ModelViewSet):

    queryset = Bug.objects.all().order_by("-created_at")

    serializer_class = BugSerializer

    pagination_class = CustomPagination

    filter_backends = [SearchFilter]

    search_fields = [
        "description",
        "actual_result"
    ]

    lookup_field = "uuid"

    def get_queryset(self):

        queryset = super().get_queryset()

        screen = self.request.query_params.get(
            "screen"
        )

        if screen:

            queryset = queryset.filter(
                screen=screen
            )

        return queryset




class TestRunVersionViewSet(ModelViewSet):

    queryset = TestRunVersion.objects.filter(
        deleted_at__isnull=True
    )

    lookup_field = "uuid"

    serializer_class = TestRunVersionSerializer

    pagination_class = CustomPagination
    
    
    from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import BulkTestCaseSerializer

from django_q.tasks import async_task


@extend_schema(
    request=BulkTestCaseSerializer(many=True),
    responses={200: None},
)
@api_view(['POST'])
def bulk_import_testcases(request):

    data = request.data

    user_id = request.user.id

    async_task(
        "apps.project.tasks.bulk_import_testcases_task",
        data,
        user_id
    )

    return Response({
        "message": "Bulk import started"
    })