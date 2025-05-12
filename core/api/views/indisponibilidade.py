from rest_framework import viewsets
from core.models import Indisponibilidade
from core.api.serializers.indisponibilidade import IndisponibilidadeSerializer
from core.api.permissions import IsAdminOrReadOnly

class IndisponibilidadeViewSet(viewsets.ModelViewSet):
    queryset = Indisponibilidade.objects.all()
    serializer_class = IndisponibilidadeSerializer
    permission_classes = [IsAdminOrReadOnly]
