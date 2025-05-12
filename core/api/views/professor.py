from rest_framework import viewsets
from core.models import Professor
from core.api.serializers.professor import ProfessorSerializer
from rest_framework.permissions import AllowAny

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [AllowAny]
