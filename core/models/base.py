import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model com timestamps de criação e atualização."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
