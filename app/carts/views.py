from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from goods.models import Products

from carts.models import Cart


def cart_add(request: HttpRequest, product_slug: str) -> HttpResponseRedirect:
    product = Products.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        carts: QuerySet[Cart] = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts[0]
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    return redirect(request.META["HTTP_REFERER"])


def cart_change(request: HttpRequest, product_slug: str) -> HttpResponse: ...


def cart_remove(request: HttpRequest, cart_id: int) -> HttpResponseRedirect:
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META["HTTP_REFERER"])
