from django.contrib import admin

# from django.utils.html import format_html
from django.utils.safestring import mark_safe


from goods.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "image_edited",
        "name",
        "slug",
        "price",
        "quantity",
        "discount",
    )
    list_editable = ("discount",)
    search_fields = (
        "name",
        "description",
    )
    list_filter = (
        "category",
        "discount",
        "quantity",
    )
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
    ]

    def image_edited(self, obj):
        if not obj.image:
            return "отсутствует"
        # return format_html(
        #     format_string=f'<img src="{obj.image.url}" width="144" height="96" style="overflow: hidden;object-fit: cover;"/>'
        # )
        return mark_safe(
            f'<img src="{obj.image.url}" width="144" height="96" style="overflow: hidden;object-fit: cover;"/>'
        )

    image_edited.short_description = "Изображение"  # type: ignore
