from rest_framework import viewsets
from core.models import Disciplina
from core.api.serializers.disciplina import DisciplinaSerializer
from core.api.permissions import IsAdminOrReadOnly

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsAdminOrReadOnly]
