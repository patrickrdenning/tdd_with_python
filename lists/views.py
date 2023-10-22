from django.shortcuts import render, redirect
from .sql_wrappers import get_all_items, create_items


def home_page(request):
    if text := request.POST.get("item_text", ""):
        create_items(text_values=[text])

    return render(
        request,
        "home.html",
    )


def view_list(request):
    items = get_all_items()
    return render(request, "list.html", {"items": items})


def new_list(request):
    create_items(text_values=[request.POST["item_text"]])
    return redirect("/lists/the-only-list-in-the-world/")
