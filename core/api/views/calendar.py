from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers.disciplina import DisciplinaSerializer
from core.api.serializers.professor import ProfessorSerializer
from core.models import Alocacao, Professor


class CalendarDataView(APIView):
    """
    Dá a hora certa pro front:
      - events: lista de aulas (disciplina+professor+horários)
      - resources: lista de professores
    """

    def get(self, request):
        profs = Professor.objects.all()
        resources = [{"id": str(p.id), "title": p.nome} for p in profs]

        alocs = Alocacao.objects.select_related(
            "disciplina", "professor"
        ).all()
        events = []
        for a in alocs:
            disc = a.disciplina
            events.append(
                {
                    "id": str(a.id),
                    "disciplina": DisciplinaSerializer(disc).data,
                    "professor": (
                        ProfessorSerializer(a.professor).data
                        if a.professor
                        else None
                    ),
                    "turma": {
                        "nome": getattr(disc, "codigo_turma", str(disc.id)),
                        "dataHoraInicio": disc.dia_semana
                        + "T"
                        + disc.horario_inicio.strftime("%H:%M:%S"),
                        "dataHoraFim": disc.dia_semana
                        + "T"
                        + disc.horario_fim.strftime("%H:%M:%S"),
                    },
                    "resourceId": str(a.professor.id) if a.professor else None,
                    "title": disc.nome,
                }
            )

        return Response({"resources": resources, "events": events})
