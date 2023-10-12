from django.db import models
from typing import NamedTuple

# Create your models here.


class Item(models.Model):
    text = models.TextField(null=True)

    class ColumnsToItemFields(NamedTuple):
        item_text: int = 1
