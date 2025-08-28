from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from goods.models import Products


def catalog(request: HttpRequest) -> HttpResponse:
    goods = Products.objects.all()
    context = {
        "title": "Home | Каталог",
        "goods": goods,
    }
    return render(request=request, template_name="goods/catalog.html", context=context)


def product(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="goods/product.html")
