from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Home | Главная",
        "content": "Магазин мебели HOME",
    }
    return render(request, "main/index.html", context)


def about(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Home | О нас",
        "content": "Магазин мебели HOME",
    }
    return render(request, "main/about.html", context)
