from django.urls import path

from carts import views

app_name = "carts"

urlpatterns = [
    path("add/", views.cart_add, name="cart_add"),
    path("change/", views.cart_change, name="cart_change"),
    path("remove/", views.cart_remove, name="cart_remove"),
]
