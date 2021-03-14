from django.db import models


class HashTable(models.Model):
    reveal = models.IntegerField()
    commitlastblock = models.IntegerField()
    commit = models.CharField(max_length=64)
    is_settle = models.BooleanField(default=False)
