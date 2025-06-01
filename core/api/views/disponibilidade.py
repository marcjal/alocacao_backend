from rest_framework import viewsets

from core.api.permissions import IsAdminOrReadOnly
from core.api.serializers.disponibilidade import DisponibilidadeSerializer
from core.models import Disponibilidade


class DisponibilidadeViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidade.objects.all()
    serializer_class = DisponibilidadeSerializer
    permission_classes = [IsAdminOrReadOnly]
