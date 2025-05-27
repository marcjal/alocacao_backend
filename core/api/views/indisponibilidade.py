from rest_framework import viewsets

from core.api.permissions import IsAdminOrReadOnly
from core.api.serializers.indisponibilidade import IndisponibilidadeSerializer
from core.models import Indisponibilidade


class IndisponibilidadeViewSet(viewsets.ModelViewSet):
    queryset = Indisponibilidade.objects.all()
    serializer_class = IndisponibilidadeSerializer
    permission_classes = [IsAdminOrReadOnly]
