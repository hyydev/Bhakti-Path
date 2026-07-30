
from django.contrib import admin
from rest_framework.permissions import IsAdminUser, AllowAny
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

schema_view = get_schema_view(
    openapi.Info(
        title="BhaktiVerse API",
        default_version="v1",
        description="API documentation for BhaktiVerse project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="devsharma13314@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[AllowAny],  # Use AllowAny for public access to the schema
)

def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('user/', include('apps.User.urls')),
    path('auth/', include('apps.Auth.urls')),
    path('product/',include('apps.ProductsManagement.urls')),
    path('order/',include('apps.Order.urls')),
    path('payments/',include('apps.Payments.urls')),



    # Swagger documentation URLs
    # Swagger/OpenAPI URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

