from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.api.views.alocacao import AlocacaoViewSet
from core.api.views.calendar import CalendarDataView
from core.api.views.dashboard import DashboardSummaryView
from core.api.views.disciplina import DisciplinaViewSet
from core.api.views.disponibilidade import DisponibilidadeViewSet
from core.api.views.export_alocacoes import ExportAlocacoesView
from core.api.views.importacao import ImportacaoViewSet
from core.api.views.professor import ProfessorViewSet

router = DefaultRouter()
router.register(r"professores", ProfessorViewSet)
router.register(r"disponibilidades", DisponibilidadeViewSet)
router.register(r"disciplinas", DisciplinaViewSet)
router.register(r"alocacoes", AlocacaoViewSet)
router.register(r"importacoes", ImportacaoViewSet)

urlpatterns = [
    path(
        "dashboard/summary/",
        DashboardSummaryView.as_view(),
        name="dashboard-summary",
    ),
    path(
        "alocacoes/export/csv/",
        ExportAlocacoesView.as_view(),
        {"format": "csv"},
        name="export-csv",
    ),
    path(
        "alocacoes/export/xlsx/",
        ExportAlocacoesView.as_view(),
        {"format": "xlsx"},
        name="export-xlsx",
    ),
    path(
        "calendar/data/",
        CalendarDataView.as_view(),
        name="calendar-data",
    ),
    path("", include(router.urls)),
]
