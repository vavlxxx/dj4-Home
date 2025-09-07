from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse

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
    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product
        )

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, product=product, quantity=1
            )

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

    cart: Cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    user_carts = get_user_carts(request)
    context: dict[str, Any] = {"carts": user_carts}

    referer = request.META.get("HTTP_REFERER", ())
    if reverse("orders:create_order") in referer:
        context["is_order_page"] = True

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html",
        context,
        request=request,
    )
    response_data = {
        "message": "Количество товара изменено",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }
    return JsonResponse(response_data)


def cart_remove(request: HttpRequest) -> JsonResponse:
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_carts = get_user_carts(request)
    context: dict[str, Any] = {"carts": user_carts}
    referer = request.META.get("HTTP_REFERER", ())
    if reverse("orders:create_order") in referer:
        context["is_order_page"] = True

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html",
        context,
        request=request,
    )
    response_data = {
        "message": "Товар удалён",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }
    return JsonResponse(response_data)
