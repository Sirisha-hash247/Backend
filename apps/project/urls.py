from django.urls import path, include

from .views import bulk_import_testcases
from rest_framework.routers import DefaultRouter
from .views import (

    bulk_import_testcases,

    ProjectViewSet,
    ModuleViewSet,
    ScreenViewSet,
    TestCaseViewSet,
    BugViewSet,
    TestRunViewSet,
    TestRunVersionViewSet,

    KPIView,
    DailyTrendView,
    FailureTrendView,
    HeatmapView,
    PassFailView,
    RecentActivityView,
    TesterProductivityView,
    RiskyModulesView,
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
    path(
        "kpis/",
        KPIView.as_view()
    ),

    path(
        "daily-trend/",
        DailyTrendView.as_view()
    ),

    path(
        "failure-trend/",
        FailureTrendView.as_view()
    ),

    path(
        "heatmap/",
        HeatmapView.as_view()
    ),

    path(
        "pass-fail/",
        PassFailView.as_view()
    ),

    path(
        "recent-activity/",
        RecentActivityView.as_view()
    ),
    path(
        "tester-productivity/",
        TesterProductivityView.as_view()
    ),

    path(
        "risky-modules/",
        RiskyModulesView.as_view()
    ),
]