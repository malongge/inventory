from django.db import models


class NoForeignKeyModel(models.Model):
    name = models.CharField(max_length=10)
