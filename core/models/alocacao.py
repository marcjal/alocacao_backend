import uuid

from django.core.validators import MinValueValidator
from django.db import models

from .base import TimeStampedModel
from .professor import Professor
from .turma import Turma


class Alocacao(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name="alocacoes",
        null=True,
        blank=True,
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name="alocacoes",
        null=True,
        blank=True,
    )
    horas_alocadas = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Carga semanal que este professor dará nesta turma",
    )
    status_conflito = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"
        unique_together = ("turma", "professor")
        ordering = ["turma"]

    def __str__(self):
        try:
            disc = self.turma.disciplina.nome
            turma = self.turma.nome
        except Exception:
            return super().__str__()

        prof = self.professor.nome if self.professor else "—sem professor—"
        return f"{disc} – {turma} → {prof}"
