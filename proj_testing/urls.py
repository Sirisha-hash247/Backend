# project urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import OrganizationViewSet, OrganizationUsersView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register('organizations', OrganizationViewSet, basename='organization')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path(
        'api/organizations/<uuid:org_id>/users/',
        OrganizationUsersView.as_view()
    ),

    path('api/users/', include('apps.users.urls')),

    path('api/', include('apps.project.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema')),
]