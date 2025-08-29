from django.db.models import Q
from . import models


def query_search(query: str):
    if query.isdigit() and len(query) <= 5:
        return models.Products.objects.filter(id=int(query))

    keywords = [word for word in query.split() if len(word) > 2]

    q_objects = Q()

    for token in keywords:
        q_objects |= Q(description__icontains=token)
        q_objects |= Q(name__icontains=token)

    return models.Products.objects.filter(q_objects)
