from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers.disciplina import DisciplinaSerializer
from core.api.serializers.professor import ProfessorSerializer
from core.models.alocacao import Alocacao
from core.models.professor import Professor


class CalendarDataView(APIView):
    """
    Retorna os dados para popular o calendário:
      - resources: lista de professores
      - events: lista de alocações (disciplina + professor + horários)
    """

    @swagger_auto_schema(
        operation_summary="Dados do calendário (recursos e eventos)",
        responses={
            200: openapi.Response(
                description="Estrutura com 'resources' e 'events'",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "resources": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="UUID do professor",
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Nome do professor",
                                    ),
                                },
                            ),
                        ),
                        "events": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="UUID da alocação",
                                    ),
                                    "disciplina": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Dados da disciplina alocada",
                                        properties={
                                            "id": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "nome": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "area": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "dia_semana": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "horario_inicio": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "horario_fim": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "carga_horaria_semanal": openapi.Schema(
                                                type=openapi.TYPE_INTEGER
                                            ),
                                            "horas_a_serem_alocadas": openapi.Schema(
                                                type=openapi.TYPE_INTEGER
                                            ),
                                        },
                                    ),
                                    "professor": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        description="Dados do professor (pode ser null)",
                                        properties={
                                            "id": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "nome": openapi.Schema(
                                                type=openapi.TYPE_STRING
                                            ),
                                            "areas": openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_STRING
                                                ),
                                            ),
                                            "carga_horaria_maxima_semanal": openapi.Schema(
                                                type=openapi.TYPE_INTEGER
                                            ),
                                            "indisponibilidades": openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_OBJECT
                                                ),
                                            ),
                                        },
                                    ),
                                    "turma": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "nome": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Nome ou código da turma",
                                            ),
                                            "dataHoraInicio": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Data e hora de início (ex: 'segundaT08:00:00')",
                                            ),
                                            "dataHoraFim": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Data e hora de fim (ex: 'segundaT10:00:00')",
                                            ),
                                        },
                                    ),
                                    "resourceId": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="UUID do professor (para FullCalendar)",
                                    ),
                                    "title": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="Título do evento (nome da disciplina)",
                                    ),
                                },
                            ),
                        ),
                    },
                ),
            )
        },
        manual_parameters=[
            openapi.Parameter(
                name="start",
                in_=openapi.IN_QUERY,
                description="Data inicial no formato YYYY-MM-DD (opcional)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                name="end",
                in_=openapi.IN_QUERY,
                description="Data final no formato YYYY-MM-DD (opcional)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    )
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
                        "dataHoraInicio": f"{disc.dia_semana}T{disc.horario_inicio.strftime('%H:%M:%S')}",
                        "dataHoraFim": f"{disc.dia_semana}T{disc.horario_fim.strftime('%H:%M:%S')}",
                    },
                    "resourceId": str(a.professor.id) if a.professor else None,
                    "title": disc.nome,
                }
            )

        return Response({"resources": resources, "events": events})
