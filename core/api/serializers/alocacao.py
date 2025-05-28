from rest_framework import serializers

from core.api.serializers.professor import ProfessorSerializer
from core.api.serializers.turma import TurmaSerializer
from core.models.alocacao import Alocacao


class AlocacaoSerializer(serializers.ModelSerializer):
    turma = TurmaSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)

    turma_id = serializers.PrimaryKeyRelatedField(
        queryset=TurmaSerializer.Meta.model.objects.all(),
        source="turma",
        write_only=True,
    )
    professor_id = serializers.PrimaryKeyRelatedField(
        queryset=ProfessorSerializer.Meta.model.objects.all(),
        source="professor",
        write_only=True,
    )

    class Meta:
        model = Alocacao
        fields = [
            "id",
            "turma",
            "professor",
            "turma_id",
            "professor_id",
            "horas_alocadas",
            "status_conflito",
            "created_at",
            "updated_at",
        ]
