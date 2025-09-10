from django.views.generic import TemplateView

# from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | Главная"
        context["content"] = "Магазин мебели HOME"
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home | О нас"
        context["content"] = "Магазин мебели HOME"
        return context


# def index(request: HttpRequest) -> HttpResponse:
#     context = {
#         "title": "Home | Главная",
#         "content": "Магазин мебели HOME",
#     }
#     return render(request, "main/index.html", context)


# def about(request: HttpRequest) -> HttpResponse:
#     context = {
#         "title": "Home | О нас",
#         "content": "Магазин мебели HOME",
#     }
#     return render(request, "main/about.html", context)
