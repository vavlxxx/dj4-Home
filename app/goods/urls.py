from django.urls import path
from django.urls.resolvers import URLPattern

from goods import views

app_name = "catalog"

urlpatterns: list[URLPattern] = [
    path("search/", views.CatalogView.as_view(), name="search"),
    path("<slug:category_slug>/", views.CatalogView.as_view(), name="index"),
    path("product/<slug:product_slug>/", views.ProductView.as_view(), name="product"),
]
