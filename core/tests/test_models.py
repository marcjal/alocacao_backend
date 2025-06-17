import pytest

from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma


@pytest.mark.django_db
def test_turma_str():
    disc = Disciplina.objects.create(nome="Historia", area="História")
    turma = Turma.objects.create(
        nome="Turma P1",
        disciplina=disc,
        dia_semana="segunda",
        horario_inicio="08:00",
        horario_fim="10:00",
    )
    assert str(turma) == "Historia – Turma P1"


@pytest.mark.django_db
def test_professor_creation():
    prof = Professor.objects.create(
        nome="Teste", areas=["X"], carga_horaria_maxima_semanal=10
    )
    assert prof.carga_horaria_maxima_semanal == 10
    assert "X" in prof.areas
