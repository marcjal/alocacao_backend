from rest_framework import viewsets

from core.api.permissions import IsAdminOrReadOnly
from core.api.serializers.disciplina import DisciplinaSerializer
from core.models.disciplina import Disciplina


class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAdminOrReadOnly]
