from django.shortcuts import render, redirect
from django.db import connection
from lists.models import Item


def home_page(request):
    if text := request.POST.get("item_text", ""):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", [text])
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM lists_item")
        items = cursor.fetchall()
        items = [Item(text=item[Item.ColumnsToItemFields.item_text]) for item in items]

    return render(
        request,
        "home.html",
        {"items": items},
    )
