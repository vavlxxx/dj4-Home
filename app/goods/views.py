from django.http import HttpRequest, HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator

from goods.utils import query_search
from goods.models import Products
from config import settings


def catalog(request: HttpRequest, category_slug: str | None = None) -> HttpResponse:
    page = int(request.GET.get("page", 1))
    order_by = request.GET.get("order_by", None)
    on_sale = request.GET.get("on_sale", None)
    q = request.GET.get("q", None)

    if category_slug and category_slug == "all":
        goods = Products.objects.all()
    elif q:
        goods = query_search(q)
    elif category_slug:
        goods = Products.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404()
    else:
        goods = Products.objects.all()

    if on_sale:
        goods = goods.filter(discount__gt=0)  # type: ignore
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)  # type: ignore

    paginator = Paginator(goods, settings.ITEMS_PER_PAGE)
    paged_goods = paginator.get_page(page)

    context = {
        "title": "Home | Каталог",
        "slug_url": category_slug,
        "goods": paged_goods,
    }
    return render(request=request, template_name="goods/catalog.html", context=context)


def product(request: HttpRequest, product_slug: str) -> HttpResponse:

    product = Products.objects.get(slug=product_slug)

    context = {
        "title": f"Home | {product.name}",
        "product": product,
    }

    return render(request=request, template_name="goods/product.html", context=context)
