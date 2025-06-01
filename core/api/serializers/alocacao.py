from rest_framework import serializers

from core.api.serializers.disciplina import DisciplinaSerializer
from core.api.serializers.professor import ProfessorSerializer
from core.models.alocacao import Alocacao
from core.models.disciplina import Disciplina
from core.models.professor import Professor


class AlocacaoSerializer(serializers.ModelSerializer):
    disciplina = DisciplinaSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(), source="disciplina", write_only=True
    )
    professor_id = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(), source="professor", write_only=True
    )

    class Meta:
        model = Alocacao
        fields = [
            "id",
            "disciplina",
            "professor",
            "disciplina_id",
            "professor_id",
            "horas_alocadas",
            "status_conflito",
            "created_at",
            "updated_at",
        ]
