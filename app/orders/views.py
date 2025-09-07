from django.http.response import HttpResponse
from django.shortcuts import render


def create_order(request) -> HttpResponse:
    return render(request, "orders/create_order.html")
