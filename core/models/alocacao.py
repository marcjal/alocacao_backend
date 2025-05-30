import uuid

from django.core.validators import MinValueValidator
from django.db import models

from .base import TimeStampedModel
from .disciplina import Disciplina
from .professor import Professor


class Alocacao(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disciplina = models.ForeignKey(
        Disciplina, on_delete=models.CASCADE, related_name="alocacoes"
    )
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name="alocacoes"
    )
    horas_alocadas = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status_conflito = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"
        indexes = [models.Index(fields=["disciplina", "professor"])]
        unique_together = ("disciplina", "professor")
        ordering = ["disciplina"]

    def __str__(self):
        return f"{self.disciplina.nome} -> {self.professor.nome}"
