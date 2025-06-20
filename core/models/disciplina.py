import uuid

from django.db import models

from .base import TimeStampedModel


class Disciplina(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, unique=True)
    area = models.CharField(max_length=100)
    creditos_academicos = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Créditos Acadêmicos (para relatórios/importações genéricas)",
    )

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
