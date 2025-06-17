import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma


@pytest.mark.django_db
def test_auto_allocation_endpoint():
    client = APIClient()
    Professor.objects.create(
        nome="Prof X", areas=["X"], carga_horaria_maxima_semanal=10
    )
    disc = Disciplina.objects.create(nome="AtvX", area="X")
    Turma.objects.create(
        nome="T1",
        disciplina=disc,
        dia_semana="segunda",
        horario_inicio="08:00",
        horario_fim="10:00",
    )

    url = reverse("alocacao-auto")
    resp = client.post(url)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status_conflito"] is False
