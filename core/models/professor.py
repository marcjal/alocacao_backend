import uuid

from django.core.validators import MinValueValidator
from django.db import models

from .base import TimeStampedModel


class Professor(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, unique=True)
    areas = models.JSONField(
        help_text="Lista de áreas/palavras-chave do professor"
    )
    carga_horaria_maxima_semanal = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Limite de horas semanais que o professor pode ministrar",
    )
    chapa = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="Matrícula ou chapa do professor (para importação)",
    )

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
