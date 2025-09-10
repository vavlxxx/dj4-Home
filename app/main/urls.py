from django.urls import path

from main import views


app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    # path("", views.index, name="index"),
    # path("about/", views.about, name="about"),
]
