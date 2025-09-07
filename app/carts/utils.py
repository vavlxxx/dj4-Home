from django.http import HttpRequest
from carts.models import Cart


def get_user_carts(request: HttpRequest):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
    return
