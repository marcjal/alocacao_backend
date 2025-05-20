"""
URL configuration for alocacao_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.api.views.export_alocacoes import ExportAlocacoesView
from core.api.views.dashboard import DashboardSummaryView

schema_view = get_schema_view(
    openapi.Info(
        title="API Alocação",
        default_version='v1',
        description="Documentação Swagger/OpenAPI para o backend de alocação",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Swagger JSON/YAML
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    # ReDoc UI (opcional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path(
        'api/v1/alocacoes/export/csv/',
        ExportAlocacoesView.as_view(),
        {'format': 'csv'},    # aqui passamos via kwargs o formato
        name='export-csv'
    ),
    path(
        'api/v1/alocacoes/export/xlsx/',
        ExportAlocacoesView.as_view(),
        {'format': 'xlsx'},   # idem, via kwargs
        name='export-xlsx'
    ),
    path('api/v1/', include('core.api.urls')),
]
