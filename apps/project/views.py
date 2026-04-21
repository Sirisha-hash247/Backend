from urllib import request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import TestCase
from .serializers import TestCaseSerializer
from .services.testcase_service import create_testcase
from .models import Bug
from .serializers import BugSerializer
from .services.bugs_service import create_bug

from core.permissions import IsAdminUserRole

from .models import Project, Module, Screen
from .serializers import ProjectSerializer, ModuleSerializer, ScreenSerializer

from .services.project_service import (
    create_project,
    get_all_projects,
    update_project,
    delete_project
)

from .services.module_service import ModuleService
from .services.screen_service import ScreenService


# ---------------- PROJECT ----------------
class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
        return get_all_projects()

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


# ---------------- MODULE ----------------
class ModuleViewSet(ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
        return ModuleService.get_all_modules()

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
        return ScreenService.get_all_screens()

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

    def get_queryset(self):
        return TestCase.objects.all()

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
    
# ---------------- BUG ----------------
class BugViewSet(ModelViewSet):
    serializer_class = BugSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_queryset(self):
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