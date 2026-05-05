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

from core.permissions import (
    IsAdminOrSuperAdmin,
    IsAdminOrTester,
    IsAdminTesterOrReviewer,
    IsTester,
    IsReviewer,
)

from .models import Project, Module, Screen, TestCase, Bug, TestRun
from .serializers import (
    ProjectSerializer, ModuleSerializer, ScreenSerializer,
    TestCaseSerializer, BugSerializer, TestRunSerializer
)
from .services.project_service import create_project, get_all_projects, update_project, delete_project
from .services.module_service import ModuleService
from .services.screen_service import ScreenService
from .services.testcase_service import create_testcase
from .services.bugs_service import create_bug
from .services.testrun_service import create_test_run

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
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        else:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]

    def get_queryset(self):
        user = self.request.user

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
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        else:
            return [IsAuthenticated(), IsAdminOrTester()]

    def get_queryset(self):
        user = self.request.user
        qs = Module.objects.filter(deleted_at__isnull=True)

        if user.role != "superadmin":
            qs = qs.filter(project__organization=user.organization)

        project_id = self.request.query_params.get("project")
        if project_id:
            qs = qs.filter(project__id=project_id)

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        module = ModuleService.create_module(request.user, serializer.validated_data)
        return Response(ModuleSerializer(module).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        module = self.get_object()
        serializer = self.get_serializer(module, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        module = ModuleService.update_module(module, request.user, serializer.validated_data)
        return Response(ModuleSerializer(module).data)

    def destroy(self, request, *args, **kwargs):
        module = self.get_object()
        ModuleService.delete_module(module, request.user)   # ✅ FIXED
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────
# SCREEN
# ─────────────────────────────────────────────
class ScreenViewSet(ModelViewSet):
    serializer_class = ScreenSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        else:
            return [IsAuthenticated(), IsAdminOrTester()]

    def get_queryset(self):
        user = self.request.user
        qs = Screen.objects.filter(deleted_at__isnull=True)

        if user.role != "superadmin":
            qs = qs.filter(module__project__organization=user.organization)

        module_id = self.request.query_params.get("module")
        if module_id:
            qs = qs.filter(module__uuid=module_id)

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        screen = ScreenService.create_screen(request.user, serializer.validated_data)
        return Response(ScreenSerializer(screen).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        screen = self.get_object()
        serializer = self.get_serializer(screen, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        screen = ScreenService.update_screen(screen, request.user, serializer.validated_data)
        return Response(ScreenSerializer(screen).data)

    def destroy(self, request, *args, **kwargs):
        screen = self.get_object()
        ScreenService.delete_screen(screen, request.user)   # ✅ FIXED
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────
# TEST CASE  —  Admin + Tester: CRU  |  Reviewer: R
# ─────────────────────────────────────────────
class TestCaseViewSet(ModelViewSet):
    serializer_class = TestCaseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        else:
            return [IsAuthenticated(), IsAdminOrTester()]

    def get_queryset(self):
        user = self.request.user
        screen_id = self.request.query_params.get("screen")

        if user.role == "superadmin":
            qs = TestCase.objects.all()
        else:
            qs = TestCase.objects.filter(
                screen__module__project__organization=user.organization
            )

        if screen_id:
            qs = qs.filter(screen__uuid=screen_id)

        return qs

    def create(self, request, *args, **kwargs):
        testcase = create_testcase(request.user, request.data)
        return Response(TestCaseSerializer(testcase).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        testcase = self.get_object()
        serializer = self.get_serializer(testcase, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        testcase = self.get_object()
        testcase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# ─────────────────────────────────────────────
# TEST RUN  —  Admin + Tester: CRU  |  Reviewer: R + comment patch
# ─────────────────────────────────────────────
class TestRunViewSet(ModelViewSet):
    serializer_class = TestRunSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'add_comment':
            # Reviewer can patch comment only
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        else:
            return [IsAuthenticated(), IsAdminOrTester()]

    def get_queryset(self):
        user = self.request.user
        screen_id = self.request.query_params.get("screen")

        if user.role == "superadmin":
            qs = TestRun.objects.all()
        else:
            qs = TestRun.objects.filter(
                test_case__screen__module__project__organization=user.organization
            )

        if screen_id:
            qs = qs.filter(test_case__screen__uuid=screen_id)

        return qs

    def create(self, request, *args, **kwargs):
        run = create_test_run(request.user, request.data)
        return Response(TestRunSerializer(run).data, status=201)

    # ✅ Reviewer-specific PATCH — only comment field
    @action(detail=True, methods=['patch'], url_path='comment')
    def add_comment(self, request, pk=None):
        run = self.get_object()
        # Only allow reviewer to patch 'actual_results' as comment
        allowed_fields = {'actual_results'}
        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        serializer = self.get_serializer(run, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)


# ─────────────────────────────────────────────
# BUG  —  Admin + Tester: CRUD  |  Reviewer: R + comment patch
# ─────────────────────────────────────────────
class BugViewSet(ModelViewSet):
    serializer_class = BugSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'add_comment':
            return [IsAuthenticated(), IsAdminTesterOrReviewer()]
        elif self.action == 'destroy':
            # Tester CAN delete bugs (CRUD), reviewer cannot
            return [IsAuthenticated(), IsAdminOrTester()]
        else:
            return [IsAuthenticated(), IsAdminOrTester()]

    def get_queryset(self):
        user = self.request.user
        screen_id = self.request.query_params.get("screen")

        if user.role == "superadmin":
            qs = Bug.objects.all()
        else:
            qs = Bug.objects.filter(
                project__organization=user.organization
            )

        if screen_id:
            qs = qs.filter(screen__uuid=screen_id)

        return qs

    def create(self, request, *args, **kwargs):
        bug = create_bug(request.user, request.data)
        return Response(BugSerializer(bug).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        bug = self.get_object()
        serializer = self.get_serializer(bug, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        bug = self.get_object()
        bug.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ✅ Reviewer-specific PATCH — only comment/status
    @action(detail=True, methods=['patch'], url_path='comment')
    def add_comment(self, request, pk=None):
        bug = self.get_object()
        allowed_fields = {'status', 'actual_results'}
        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        serializer = self.get_serializer(bug, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=request.user)
        return Response(serializer.data)
    
    
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from .models import TestCase




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

    return Response({"message": "Bulk import started"})


