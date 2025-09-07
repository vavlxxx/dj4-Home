from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from goods.models import Products

# from carts.models import Cart


def cart_add(request: HttpRequest, product_slug: str) -> HttpResponse: ...


def cart_change(request: HttpRequest, product_slug: str) -> HttpResponse: ...


def cart_remove(request: HttpRequest, product_slug: str) -> HttpResponse: ...
