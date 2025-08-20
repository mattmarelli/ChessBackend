from django.db import models

class ActivesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)

    actives = ActivesManager()

    class Meta:
        abstract = True
