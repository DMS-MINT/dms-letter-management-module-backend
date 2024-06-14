from django.db import models

from core.common.models import BaseModel


class Permission(BaseModel):
    name = models.CharField(max_length=10, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
