# api_auth/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.shortcuts import redirect

schema_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version='v1',
        description="API documentation for authentication system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/', include('authentication.urls')),  # Make sure this is correct
    path('', lambda request: redirect('schema-swagger-ui')),
    path('admin/', admin.site.urls),
    path('swagger/', ensure_csrf_cookie(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
