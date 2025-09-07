from django.urls import path
from django.urls.resolvers import URLPattern

from carts import views

app_name = "carts"

urlpatterns: list[URLPattern] = [
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("change/<int:product_id>/", views.cart_change, name="cart_change"),
    path("remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
]
