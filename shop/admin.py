from django.contrib import admin
from .models import *


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    # extra = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImagesInline,
    ]


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
admin.site.register(Brand)
admin.site.register(Category)



