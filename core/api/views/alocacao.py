from rest_framework import viewsets
from core.models import Alocacao
from core.api.serializers.alocacao import AlocacaoSerializer
from core.api.permissions import IsAdminOrReadOnly

class AlocacaoViewSet(viewsets.ModelViewSet):
    queryset = Alocacao.objects.all()
    serializer_class = AlocacaoSerializer
    permission_classes = [IsAdminOrReadOnly]
