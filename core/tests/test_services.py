from datetime import time

import pytest

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma
from core.services.allocation import run_allocation


@pytest.mark.django_db
def test_run_allocation_creates_allocations():
    Professor.objects.create(
        nome="Prof A", areas=["A"], carga_horaria_maxima_semanal=10
    )
    Professor.objects.create(
        nome="Prof B", areas=["B"], carga_horaria_maxima_semanal=10
    )
    disc_a = Disciplina.objects.create(nome="AtvA", area="A")
    disc_b = Disciplina.objects.create(nome="AtvB", area="B")
    Turma.objects.create(
        nome="T1",
        disciplina=disc_a,
        dia_semana="segunda",
        horario_inicio=time(8),
        horario_fim=time(10),
    )
    Turma.objects.create(
        nome="T2",
        disciplina=disc_b,
        dia_semana="terça",
        horario_inicio=time(8),
        horario_fim=time(10),
    )

    alocs = run_allocation(recalculate_all=True)
    assert len(alocs) == 2
    assert Alocacao.objects.count() == 2

    areas = {a.professor.areas[0] for a in alocs}
    assert areas == {"A", "B"}
