from django.db import models

from .models import Product, Category


def category_processor(request):
    cat_man = Category.objects.filter(product__gender='man').annotate(n=models.Count("pk"))
    cat_woman = Category.objects.filter(product__gender='woman').annotate(n=models.Count("pk"))
    context = {
        'man': cat_man,
        'woman': cat_woman,
    }
    return context
