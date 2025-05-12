from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from core.services.allocation import run_allocation
from core.models import Alocacao
from core.api.serializers.alocacao import AlocacaoSerializer

class AlocacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AlocacaoSerializer
    queryset = Alocacao.objects.all()

    @action(detail=False, methods=['post'])
    def auto(self, request):
        alocs = run_allocation()
        serializer = self.get_serializer(alocs, many=True)
        return Response(serializer.data)
