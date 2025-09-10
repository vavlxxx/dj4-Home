from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("registration/", views.UserRegistrationView.as_view(), name="registration"),
    path("profile/", views.UserUpdateView.as_view(), name="profile"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("cart/", views.UserCartView.as_view(), name="cart"),
]
