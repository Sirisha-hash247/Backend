from django.urls import path, include

from .views import bulk_import_testcases
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    ModuleViewSet,
    ScreenViewSet,
    TestCaseViewSet,
    BugViewSet,
    TestRunViewSet,
    TestRunVersionViewSet,
)

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('modules', ModuleViewSet, basename='module')
router.register('screens', ScreenViewSet, basename='screen')
router.register('testcases', TestCaseViewSet, basename='testcase')
router.register('bugs', BugViewSet, basename='bug')
router.register('testruns', TestRunViewSet, basename='testrun')
router.register(
    r'testrun-versions',
    TestRunVersionViewSet,
    basename='testrun-versions'
)



urlpatterns = [
    path('testcases/bulk-import/', bulk_import_testcases),  
    path("", include(router.urls)),
]