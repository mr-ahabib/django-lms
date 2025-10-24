from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version='v1',
        description="Learning Management System API",
        contact=openapi.Contact(email="contact@lms.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Your app endpoints
    path("api/users/", include("users.urls")),
    path("api/", include("courses.urls")),
    path("api/", include("enrollments.urls")),

    # Swagger endpoints
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
