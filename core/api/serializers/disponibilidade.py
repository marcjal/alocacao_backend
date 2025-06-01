from rest_framework import serializers

from core.models.disponibilidade import Disponibilidade


class DisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidade
        fields = [
            "id",
            "professor",
            "dia_semana",
            "horario_inicio",
            "horario_fim",
        ]
