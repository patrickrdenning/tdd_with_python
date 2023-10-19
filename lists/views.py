from django.shortcuts import render, redirect
from django.db import connection
from lists.models import Item


def home_page(request):
    if text := request.POST.get("item_text", ""):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", [text])
        return redirect("/lists/the-only-list-in-the-world/")


    return render(
        request,
        "home.html",
    )


def view_list(request):
    items = select_all_items()
    return render(request, "list.html", {"items": items})


def select_all_items() -> list:
    # TODO: extent to take an optional sub set of columns to select
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM lists_item")
        rows = cursor.fetchall()
        model_instances = [Item(text=row[Item.ITEM_FIELDS_TO_COLUMNS["text"]]) for row in rows]

    return model_instances
