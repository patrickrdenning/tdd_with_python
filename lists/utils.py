from django.db import connection
from lists.models import Item



def select_all_items() -> list:
    # TODO: extent to take an optional sub set of columns to select
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM lists_item")
        rows = cursor.fetchall()
        model_instances = [Item(text=row[Item.ITEM_FIELDS_TO_COLUMNS["text"]]) for row in rows]

    return model_instances