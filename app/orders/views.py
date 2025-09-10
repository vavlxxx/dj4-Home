from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.utils import create_order
from users.models import User
from orders.forms import CreateOrderForm


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("users:profile")

    def get_initial(self):
        initial = super().get_initial()
        user: User = self.request.user  # type: ignore
        initial["first_name"] = user.first_name
        initial["last_name"] = user.last_name
        initial["email"] = user.email
        return initial

    def form_valid(self, form):
        create_order(self.request, form)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Заполните все обязательные поля")
        return redirect("orders:create_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Оформление заказа"
        context["is_order_page"] = True
        return context


# @login_required
# def create_order(request):
#     if request.method == "POST":
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=user)

#                     if cart_items.exists():
#                         # Создать заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data["phone_number"],
#                             requires_delivery=form.cleaned_data["requires_delivery"],
#                             delivery_address=form.cleaned_data["delivery_address"],
#                             payment_on_get=form.cleaned_data["payment_on_get"],
#                         )
#                         # Создать заказанные товары
#                         for cart_item in cart_items:
#                             product = cart_item.product
#                             name = cart_item.product.name
#                             price = cart_item.product.sell_price()
#                             quantity = cart_item.quantity

#                             if product.quantity < quantity:
#                                 raise ValidationError(
#                                     f"Недостаточное количество товара {name} на складе\
#                                                        В наличии - {product.quantity}"
#                                 )

#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save()

#                         # Очистить корзину пользователя после создания заказа
#                         cart_items.delete()

#                         messages.success(request, "Заказ оформлен!")
#                         return redirect("users:profile")
#             except ValidationError as e:
#                 messages.warning(request, str(e))
#                 return redirect("orders:create_order")
#     else:
#         initial = {
#             "first_name": request.user.first_name,
#             "last_name": request.user.last_name,
#         }

#         form = CreateOrderForm(initial=initial)

#     context = {
#         "title": "Home - Оформление заказа",
#         "form": form,
#         "is_order_page": True,
#     }
#     return render(request, "orders/create_order.html", context=context)
