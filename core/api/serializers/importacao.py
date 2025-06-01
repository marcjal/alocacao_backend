from rest_framework import serializers

from core.models.importacao import Importacao


class ImportacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importacao
        fields = [
            "id",
            "tipo",
            "file",
            "status",
            "registros_total",
            "registros_sucesso",
            "registros_erro",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "status",
            "registros_total",
            "registros_sucesso",
            "registros_erro",
            "created_at",
            "updated_at",
        ]
