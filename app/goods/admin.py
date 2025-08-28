from django.contrib import admin
from django.utils.html import format_html

from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("image_edited", "name", "slug")

    def image_edited(self, obj):
        if not obj.image:
            return "отсутствует"
        return format_html(
            f'<img src="{obj.image.url}" width="144" height="96" style="overflow: hidden;object-fit: cover;"/>'
        )

    image_edited.short_description = "Изображение"  # type: ignore
