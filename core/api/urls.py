from rest_framework.routers import DefaultRouter

from core.api.views.alocacao import AlocacaoViewSet
from core.api.views.disciplina import DisciplinaViewSet
from core.api.views.disponibilidade import DisponibilidadeViewSet
from core.api.views.importacao import ImportacaoViewSet
from core.api.views.professor import ProfessorViewSet

router = DefaultRouter()
router.register(r"professores", ProfessorViewSet)
router.register(r"disponibilidades", DisponibilidadeViewSet)
router.register(r"disciplinas", DisciplinaViewSet)
router.register(r"alocacoes", AlocacaoViewSet)
router.register(r"importacoes", ImportacaoViewSet)

urlpatterns = router.urls
