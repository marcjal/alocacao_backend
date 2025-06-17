import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma


@pytest.mark.django_db
def test_dashboard_summary_counts():
    client = APIClient()

    Disciplina.objects.bulk_create(
        [
            Disciplina(nome="D1", area="A"),
            Disciplina(nome="D2", area="B"),
        ]
    )
    Professor.objects.bulk_create(
        [
            Professor(nome="P1", areas=["A"], carga_horaria_maxima_semanal=5),
            Professor(nome="P2", areas=["B"], carga_horaria_maxima_semanal=5),
            Professor(nome="P3", areas=["C"], carga_horaria_maxima_semanal=5),
        ]
    )
    turma = Turma.objects.create(
        nome="T1",
        disciplina=Disciplina.objects.first(),
        dia_semana="segunda",
        horario_inicio="08:00",
        horario_fim="10:00",
    )
    Alocacao.objects.create(
        turma=turma,
        professor=Professor.objects.first(),
        horas_alocadas=2,
        status_conflito=True,
    )

    url = reverse("dashboard-summary")
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_disciplinas"] == 2
    assert data["total_professores"] == 3
    assert data["total_conflitos"] == 1
