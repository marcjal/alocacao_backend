from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Alocacao, Disciplina, Professor


class DashboardSummaryView(APIView):
    """
    Retorna o total de disciplinas, total de professores e total de alocações em conflito.
    """

    @swagger_auto_schema(
        operation_summary="Resumo de contadores para o dashboard",
        responses={
            200: openapi.Response(
                description="Totais de disciplinas, professores e conflitos",
                examples={
                    "application/json": {
                        "total_disciplinas": 12,
                        "total_professores": 5,
                        "total_conflitos": 2,
                    }
                },
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "total_disciplinas": openapi.Schema(
                            type=openapi.TYPE_INTEGER
                        ),
                        "total_professores": openapi.Schema(
                            type=openapi.TYPE_INTEGER
                        ),
                        "total_conflitos": openapi.Schema(
                            type=openapi.TYPE_INTEGER
                        ),
                    },
                ),
            )
        },
    )
    def get(self, request):
        total_disciplinas = Disciplina.objects.count()
        total_professores = Professor.objects.count()
        total_conflitos = Alocacao.objects.filter(status_conflito=True).count()

        return Response(
            {
                "total_disciplinas": total_disciplinas,
                "total_professores": total_professores,
                "total_conflitos": total_conflitos,
            },
            status=status.HTTP_200_OK,
        )
