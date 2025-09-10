from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.models import Order, OrderItem
from carts.models import Cart
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    # success_url = reverse_lazy("main:index")

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page is not None and redirect_page != reverse("users:logout"):
            return redirect_page
        return reverse_lazy("main:index")

    def form_valid(self, form):  # type: ignore
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            auth.login(self.request, user)
            messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")  # type: ignore
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Авторизация"
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):  # type: ignore
        session_key = self.request.session.session_key
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(
                self.request,
                f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт",
            )
            return HttpResponseRedirect(self.success_url)  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Регистрация"
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):  # type: ignore
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Профайл не обновлен")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Кабинет"
        context["orders"] = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
            .order_by("-id")
        )
        return context


class UserCartView(LoginRequiredMixin, TemplateView):
    template_name = "users/users_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Корзина"
        return context


class UserLogoutView(LogoutView):
    success_url = reverse_lazy("main:index")

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")  # type: ignore
        return super().post(request, *args, **kwargs)


# @login_required
# def logout(request):
#     messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
#     auth.logout(request)
#     return redirect(reverse("main:index"))


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)
#             session_key = request.session.session_key

#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f"{username}, Вы вошли в аккаунт")

#                 if session_key:
#                     forgot_carts = Cart.objects.filter(user=user)
#                     if forgot_carts.exists():
#                         forgot_carts.delete()
#                     Cart.objects.filter(session_key=session_key).update(user=user)

#                 redirect_page = request.POST.get("next", None)
#                 if redirect_page is not None and redirect_page != reverse(
#                     "users:logout"
#                 ):
#                     return HttpResponseRedirect(redirect_page)
#                 return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserLoginForm()

#     context = {"title": "Home | Авторизация", "form": form}
#     return render(request, "users/login.html", context)


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         session_key = request.session.session_key

#         if form.is_valid():
#             form.save()
#             user = form.instance
#             auth.login(request, user)
#             messages.success(
#                 request,
#                 f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт",
#             )

#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)

#             return HttpResponseRedirect(reverse("main:index"))
#     else:
#         form = UserRegistrationForm()

#     context = {"title": "Home | Регистрация", "form": form}
#     return render(request, "users/registration.html", context)


# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = ProfileForm(
#             data=request.POST, instance=request.user, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Профайл успешно обновлен")
#             return HttpResponseRedirect(reverse("users:profile"))
#     else:
#         form = ProfileForm(instance=request.user)

#     orders = (
#         Order.objects.filter(user=request.user)
#         .prefetch_related(
#             Prefetch(
#                 "orderitem_set",
#                 queryset=OrderItem.objects.select_related("product"),
#             )
#         )
#         .order_by("-id")
#     )
#     context = {"title": "Home | Кабинет", "form": form, "orders": orders}
#     return render(request, "users/profile.html", context)


# @login_required
# def cart(request):
#     return render(request=request, template_name="users/users_cart.html")
