from django.shortcuts import render, redirect
from django.db import connection
from .utils import select_all_items

def home_page(request):
    if text := request.POST.get("item_text", ""):  # Is this going to break if a non-post request is received?
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






