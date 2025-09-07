from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string

from carts.utils import get_user_carts
from goods.models import Products
from carts.models import Cart


def cart_add(request: HttpRequest) -> JsonResponse:
    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)
    if request.user.is_authenticated:
        carts: QuerySet[Cart] = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts[0]
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    user_carts = get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html",
        {"carts": user_carts},
        request=request,
    )
    response_data = {
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)


def cart_change(request: HttpRequest) -> JsonResponse:
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()

    user_carts = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html",
        {"carts": user_carts},
        request=request,
    )
    response_data = {
        "message": "Количество товара изменено",
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)


def cart_remove(request: HttpRequest) -> JsonResponse:
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()
    user_carts = get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html",
        {"carts": user_carts},
        request=request,
    )
    response_data = {
        "message": "Товар удалён",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }
    return JsonResponse(response_data)
