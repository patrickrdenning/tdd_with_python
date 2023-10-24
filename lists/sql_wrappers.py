from django.db import connection


def get_all(table: str) -> list:
    # TODO: extend to take an optional sub set of columns to select
    # TODO: extend to take an optional table name to select all rows of an arbitrary table
    with connection.cursor() as cursor:
        ensure_table_exists_with_column(connection, table)
        cursor.execute(f"SELECT * FROM lists_{table}")
        data = fetch_rows_with_column_names(cursor)

    return data


def create_items(text_values: list) -> None:
    with connection.cursor() as cursor:
        ensure_table_exists_with_column(connection, "lists_item", "text")
        for text_value in text_values:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", [text_value])


def fetch_rows_with_column_names(cursor) -> list:
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def ensure_table_exists_with_column(connection, table: str, column: str = None) -> None:
    if table not in connection.introspection.table_names():
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE TABLE {table} (id INT PRIMARY KEY, {column} TEXT);")
    if column and column not in [
        column.name
        for column in connection.introspection.get_table_description(
            connection.cursor(), table
        )
    ]:
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT;")
