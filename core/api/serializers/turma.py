from rest_framework import serializers

from core.api.serializers.disciplina import DisciplinaSerializer
from core.models.turma import Turma


class TurmaSerializer(serializers.ModelSerializer):
    disciplina = DisciplinaSerializer(read_only=True)
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=DisciplinaSerializer.Meta.model.objects.all(),
        source="disciplina",
        write_only=True,
    )

    class Meta:
        model = Turma
        fields = [
            "id",
            "nome",
            "disciplina",
            "disciplina_id",
            "local",
            "dia_semana",
            "horario_inicio",
            "horario_fim",
            "created_at",
            "updated_at",
        ]
