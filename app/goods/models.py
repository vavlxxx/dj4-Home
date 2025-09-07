from decimal import Decimal

from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="SLUG"
    )

    @classmethod
    def get_default(cls):
        obj, _ = cls.objects.get_or_create(name="Без категории")
        return obj.id  # type: ignore

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "categories"


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="SLUG"
    )
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="goods_images", null=True, blank=True, verbose_name="Изображение"
    )
    price = models.DecimalField(
        default=Decimal(0.0), max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    discount = models.DecimalField(
        default=Decimal(0.0), max_digits=4, decimal_places=2, verbose_name="Скидка (%)"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(
        to=Categories,
        on_delete=models.SET_DEFAULT,
        default=Categories.get_default,
        verbose_name="Категория",
    )

    def display_id(self) -> str:
        return f"{self.id:07}"  # type: ignore

    def sell_price(self) -> Decimal:
        if self.discount:
            return round(self.price - (self.price * self.discount / 100), 2)
        return self.price

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        db_table = "products"
        ordering = ("id",)
