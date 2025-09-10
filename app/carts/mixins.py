from django.template.loader import render_to_string
from django.urls import reverse

from carts.utils import get_user_carts
from goods.models import Products
from carts.models import Cart


class CartMixin:
    def get_cart(
        self, request, product: Products | None = None, cart_id: int | None = None
    ) -> Cart:
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product
        if cart_id:
            query_kwargs["id"] = cart_id

        return Cart.objects.filter(**query_kwargs).first()  # type: ignore

    def render_cart(self, request):
        user_cart = get_user_carts(request)
        context: dict = {"carts": user_cart}

        referer = request.META.get("HTTP_REFERER", ())
        if reverse("orders:create_order") in referer:
            context["is_order_page"] = True

        return render_to_string(
            "carts/includes/included_cart.html", {"carts": user_cart}
        )
