from django.db import models
from typing import NamedTuple

# Create your models here.


class Item(models.Model):
    text = models.TextField(null=True)

    ITEM_FIELDS_TO_COLUMNS = {"text": 1}
