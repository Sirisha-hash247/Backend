# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ProjectViewSet


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ModuleViewSet, ScreenViewSet   # ✅ IMPORTANT

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('modules', ModuleViewSet, basename='module')   # ✅ FIX
router.register('screens', ScreenViewSet, basename='screen')

urlpatterns = [
    path('', include(router.urls)),
]


# router = DefaultRouter()
# router.register('', ProjectViewSet, basename='projects')
# router.register('modules', ModuleViewSet)
# router.register('screens', ScreenViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

