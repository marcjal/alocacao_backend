from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Disciplina, Professor, Alocacao

class DashboardSummaryView(APIView):
    """
    Retorna o total de disciplinas, total de professores e total de alocações em conflito.
    """

    def get(self, request):
        total_disciplinas = Disciplina.objects.count()
        total_professores = Professor.objects.count()
        total_conflitos = Alocacao.objects.filter(status_conflito=True).count()

        return Response({
            "total_disciplinas": total_disciplinas,
            "total_professores": total_professores,
            "total_conflitos": total_conflitos
        }, status=status.HTTP_200_OK)
