import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor
from core.models.turma import Turma


@pytest.mark.django_db
def test_export_csv_download():
    client = APIClient()
    disc = Disciplina.objects.create(nome="DX", area="Z")
    prof = Professor.objects.create(
        nome="PX", areas=["Z"], carga_horaria_maxima_semanal=5
    )
    turma = Turma.objects.create(
        nome="TX",
        disciplina=disc,
        dia_semana="sexta",
        horario_inicio="09:00",
        horario_fim="11:00",
    )
    Alocacao.objects.create(
        turma=turma, professor=prof, horas_alocadas=2, status_conflito=False
    )

    url = reverse("export-csv", kwargs={"format": "csv"})
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp["Content-Type"] == "text/csv"
    body = resp.content.decode()

    assert "Código atividade" in body
    assert "PX" in body
