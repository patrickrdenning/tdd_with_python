from django.shortcuts import render, redirect
from django.db import connection


def home_page(request):
    if text := request.POST.get("item_text", ""):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lists_item (text) VALUES (%s)", [text])
        return redirect("/")

    return render(
        request,
        "home.html",
    )
