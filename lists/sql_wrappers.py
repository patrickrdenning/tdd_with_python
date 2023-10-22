from django.db import connection
from lists.models import Item


def get_all_items() -> list:
    # TODO: extend to take an optional sub set of columns to select
    # TODO: extend to take an optional table name to select all rows of an arbitrary table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM lists_item")
        rows = cursor.fetchall()
        model_instances = [
            Item(text=row[Item.ITEM_FIELDS_TO_COLUMNS["text"]]) for row in rows
        ]

    return model_instances


def create_items(text_values: list) -> None:
    with connection.cursor() as cursor:
        for text_value in text_values:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", [text_value])
