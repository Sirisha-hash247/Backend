from urllib import request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import TestCase, TestRun
from .serializers import TestCaseSerializer
from .services.testcase_service import create_testcase
from .models import Bug
from .serializers import BugSerializer
from .services.bugs_service import create_bug
from .services.testrun_service import create_test_run

from core.permissions import IsAdminUserRole, IsAdminOrSuperAdmin

from .models import Project, Module, Screen
from .serializers import ProjectSerializer, ModuleSerializer, ScreenSerializer, TestRunSerializer

from .services.project_service import (
    create_project,
    get_all_projects,
    update_project,
    delete_project
)

from .services.module_service import ModuleService
from .services.screen_service import ScreenService

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def get_queryset(self):
        return get_all_projects(self.request.user)

    # CREATE PROJECT (AUTO ORG)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project = create_project(request.user, serializer.validated_data)

        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = self.get_object()

        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            project = update_project(project, request.user, serializer.validated_data)
        except PermissionError as e:
            return Response({"error": str(e)}, status=403)

        return Response(ProjectSerializer(project).data)

    #  DELETE WITH SECURITY
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        try:
            delete_project(project, request.user)
        except PermissionError as e:
            return Response({"error": str(e)}, status=403)

        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------- MODULE ----------------
class ModuleViewSet(ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
        project_id = self.request.query_params.get("project")

        if project_id:
            return Module.objects.filter(project__id=project_id)

        return Module.objects.all()

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
        ModuleService.delete_module(module)

        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------- SCREEN ----------------
class ScreenViewSet(ModelViewSet):
    serializer_class = ScreenSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
        module_id = self.request.query_params.get("module")

        if module_id:
            return Screen.objects.filter(module__uuid=module_id)

        return Screen.objects.all()

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
        ScreenService.delete_screen(screen)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ---------------- TEST CASE ----------------
class TestCaseViewSet(ModelViewSet):
    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    # 🔥 UPDATED QUERYSET (IMPORTANT)
    def get_queryset(self):
        screen_id = self.request.query_params.get("screen")

        if screen_id:
            return TestCase.objects.filter(screen__uuid=screen_id)

        return TestCase.objects.all()

    # ➕ CREATE
    def create(self, request, *args, **kwargs):
        testcase = create_testcase(request.user, request.data)
        return Response(
            TestCaseSerializer(testcase).data,
            status=status.HTTP_201_CREATED
        )

    # ✏️ UPDATE
    def update(self, request, *args, **kwargs):
        testcase = self.get_object()

        serializer = self.get_serializer(
            testcase,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        serializer.save(updated_by=request.user)

        return Response(serializer.data)

    # ❌ DELETE
    def destroy(self, request, *args, **kwargs):
        testcase = self.get_object()
        testcase.delete()

        return Response(status=status.HTTP_204_NO_CONTENT) 
# ---------------- BUG ----------------
class BugViewSet(ModelViewSet):
    serializer_class = BugSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
        screen_id = self.request.query_params.get("screen")

        if screen_id:
            return Bug.objects.filter(screen__uuid=screen_id)

        return Bug.objects.all()

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
    
class TestRunViewSet(ModelViewSet):
    serializer_class = TestRunSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        screen_id = self.request.query_params.get("screen")

        if screen_id:
            return TestRun.objects.filter(
                test_case__screen__uuid=screen_id
            )

        return TestRun.objects.all()

    def create(self, request, *args, **kwargs):
        run = create_test_run(request.user, request.data)
        return Response(TestRunSerializer(run).data, status=201)