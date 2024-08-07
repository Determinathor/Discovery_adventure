from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import *  #(Model, CharField, ForeignKey, DO_NOTHING,
from django.core.validators import MinValueValidator
from django.urls import reverse

from accounts.models import Profile


class Manufacturer(Model):
    name = CharField(max_length=80, null=True, blank=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"<Manufacturer: {self.name}>"

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=42, null=True, blank=False)
    thumbnail = models.CharField(max_length=200, blank=True, null=True)  # Cesta k obrázku

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError("Name must be at least 2 characters")


class Product(models.Model):
    class ProductType(models.TextChoices):
        SHOES = 'BT', 'Boty'
        CLOTHES = 'OB', 'Oblečení'
        ACCESSORIES = 'ACS', 'Příslušenství'
        OTHER = 'OT', 'Jiné'

    title = models.CharField(max_length=100, null=True, blank=False)
    product_type = models.CharField(
        max_length=3,
        choices=ProductType.choices,
        default=ProductType.OTHER,
    )
    description = models.CharField(max_length=500, null=True, blank=False)
    thumbnail = models.CharField(max_length=200, blank=True, null=True)  # Cesta k obrázku
    price = models.IntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(1)])
    stock = models.IntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(0)])
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.DO_NOTHING, null=True, blank=False)
    categories = models.ManyToManyField('Category', related_name='products', blank=True)

    class Meta:
        ordering = ['title', 'stock', 'price']

    def __str__(self):
        return f"{self.title}, in stock: {self.stock}, price: {self.price} EUR"

    def __repr__(self):
        return f"<Product: {self.title}, in stock: {self.stock}, price: {self.price} EUR>"

    def add_to_cart_url(self):
        return reverse("add_to_cart", kwargs=
        {"pk": self.pk
         })

    def clean(self):
        if self.price <= 0:
            raise ValidationError('Price must be greater than 0.')
        if self.stock < 0:
            raise ValidationError('Stock cannot be negative.')


class Cart(Model):
    quantity = IntegerField(default=0, null=True, blank=False)
    Product = ManyToManyField(Product, related_name='cart')


class Order(Model):
    total_cost = IntegerField(default=0, null=True, blank=False)
    delivery_address = CharField(max_length=100, null=True, blank=False)
    date_of_sale = DateField(null=True, blank=False)
    status = CharField(max_length=42, null=True, blank=False)
    User = ForeignKey(Profile, on_delete=DO_NOTHING, null=True, blank=False)

    def clean(self):
        if self.total_cost < 0:
            raise ValidationError('Total cost cannot be negative.')


class Order_Line(Model):
    product_price = IntegerField(default=0, null=True, blank=False)
    quantity = IntegerField(default=1, null=True, blank=False)
    Product = ForeignKey(Product, on_delete=DO_NOTHING, null=True, blank=False)
    Order = ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)

    def total_order_line_price(self):
        return self.product_price * self.quantity

    total_order_line_price.short_description = 'Total Price'


class Payment(Model):
    Order = ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)
    date_of_payment = DateTimeField(null=True, blank=False)