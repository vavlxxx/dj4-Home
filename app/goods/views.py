from django.http import Http404
from django.views.generic import DetailView, ListView

from goods.utils import query_search
from goods.models import Products
from config import settings


class CatalogView(ListView):
    model = Products
    template_name = "goods/catalog.html"
    # queryset = Products.objects.all()
    context_object_name = "goods"
    paginate_by = settings.ITEMS_PER_PAGE
    slug_url_kwarg = "category_slug"
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        # page = int(self.request.GET.get("page", 1))
        order_by = self.request.GET.get("order_by", None)
        on_sale = self.request.GET.get("on_sale", None)
        q = self.request.GET.get("q", None)

        if category_slug and category_slug == "all":
            goods = super().get_queryset()
        elif q:
            goods = query_search(q)
        elif category_slug:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
        else:
            goods = super().get_queryset()

        if on_sale:
            goods = goods.filter(discount__gt=0)  # type: ignore
        if order_by and order_by != "default":
            goods = goods.order_by(order_by)  # type: ignore
        return goods

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["title"] = "Home | Каталог"
        context["goods"] = context["page_obj"]
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        return context


class ProductView(DetailView):
    # model = Products
    # slug_field = "slug"
    # queryset = Products.objects.all()
    template_name = "goods/product.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context


# def catalog(request: HttpRequest, category_slug: str | None = None) -> HttpResponse:
#     page = int(request.GET.get("page", 1))
#     order_by = request.GET.get("order_by", None)
#     on_sale = request.GET.get("on_sale", None)
#     q = request.GET.get("q", None)

#     if category_slug and category_slug == "all":
#         goods = Products.objects.all()
#     elif q:
#         goods = query_search(q)
#     elif category_slug:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()
#     else:
#         goods = Products.objects.all()

#     if on_sale:
#         goods = goods.filter(discount__gt=0)  # type: ignore
#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)  # type: ignore

#     paginator = Paginator(goods, settings.ITEMS_PER_PAGE)
#     paged_goods = paginator.get_page(page)

#     context = {
#         "title": "Home | Каталог",
#         "slug_url": category_slug,
#         "goods": paged_goods,
#     }
#     return render(request=request, template_name="goods/catalog.html", context=context)


# def product(request: HttpRequest, product_slug: str) -> HttpResponse:

#     product = Products.objects.get(slug=product_slug)

#     context = {
#         "title": f"Home | {product.name}",
#         "product": product,
#     }

#     return render(request=request, template_name="goods/product.html", context=context)
