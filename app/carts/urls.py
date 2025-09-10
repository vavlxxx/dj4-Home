from django.urls import path

from carts import views

app_name = "carts"

urlpatterns = [
    path("add/", views.CartAddView.as_view(), name="cart_add"),
    path("change/", views.CartUpdateView.as_view(), name="cart_change"),
    path("remove/", views.CartRemoveView.as_view(), name="cart_remove"),
]
