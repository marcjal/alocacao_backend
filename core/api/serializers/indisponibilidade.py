from rest_framework import serializers

from core.models import Indisponibilidade


class IndisponibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indisponibilidade
        fields = ["id", "professor", "dia_semana", "horario_inicio", "horario_fim"]
