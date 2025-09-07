from django.db.models.query import QuerySet
from django.http import HttpRequest
from carts.models import Cart


def get_user_carts(request: HttpRequest) -> QuerySet[Cart, Cart]:
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related("product")
    if request.session.session_key is None:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).select_related(
        "product"
    )
