from datetime import date
from django.db import models
from django.db.models import *  # Importujeme všechny základní modelové třídy
from django.core.validators import MinValueValidator
from django.urls import reverse

from accounts.models import Profile


# Model pro výrobce
class Manufacturer(models.Model):
    name = models.CharField(max_length=80, null=True, blank=False)  # Název výrobce

    class Meta:
        ordering = ['name']  # Řazení podle názvu výrobce

    def __repr__(self):
        return f"<Manufacturer: {self.name}>"

    def __str__(self):
        return f"{self.name}"


# Model pro kategorii produktu
class Category(models.Model):
    name = models.CharField(max_length=42, null=True, blank=False)  # Název kategorie

    class Meta:
        ordering = ['name']  # Řazení podle názvu kategorie
        verbose_name_plural = 'Categories'  # Plurální název pro zobrazení v administraci

    def __str__(self):
        return self.name


# Model pro produkt
class Product(models.Model):
    # Typ produktu (výběrové možnosti)
    class ProductType(models.TextChoices):
        SHOES = 'BT', 'Boty'
        CLOTHES = 'OB', 'Oblečení'
        ACCESSORIES = 'ACS', 'Příslušenství'
        OTHER = 'OT', 'Jiné'

    title = models.CharField(max_length=100, null=True, blank=False)  # Název produktu
    product_type = models.CharField(
        max_length=3,
        choices=ProductType.choices,
        default=ProductType.OTHER,  # Výchozí typ produktu
    )
    description = models.CharField(max_length=500, null=True, blank=False)  # Popis produktu
    thumbnail = models.CharField(max_length=500, null=True, blank=False)  # Odkaz na obrázek produktu
    price = models.IntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(1)])  # Cena produktu
    stock = models.IntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(0)])  # Množství na sklade
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.DO_NOTHING, null=True, blank=False)  # Výrobce produktu
    categories = models.ManyToManyField('Category', related_name='products', blank=True)  # Kategorie produktu
    # created_at = models.DateTimeField(auto_now_add=True, null=True, blank=False)  # TODO: Přidat čas vytvoření

    class Meta:
        ordering = ['title', 'stock', 'price']  # Řazení podle názvu, množství a ceny

    def __str__(self):
        return f"{self.title}, in stock: {self.stock}, price: {self.price} EUR"

    def __repr__(self):
        return f"<Product: {self.title}, in stock: {self.stock}, price: {self.price} EUR>"

    def add_to_cart_url(self):
        return reverse("add_to_cart", kwargs=
        {"pk": self.pk
         })


class Cart(Model):
    quantity = IntegerField(default=0, null=True, blank=False)
    Product = ManyToManyField(Product, related_name='cart')


# class Category(Model):
#     name = CharField(max_length=42, null=True, blank=False)
#     Product = ManyToManyField(Product, related_name='category', blank=True)
#
#     class Meta:
#         ordering = ['name']
#         verbose_name_plural = 'Categories'

    # def __str__(self):
    #     return f"{self.name}"


class Order(Model):
    total_cost = IntegerField(default=0, null=True, blank=False)
    delivery_address = CharField(max_length=100, null=True, blank=False)
    # user_address = CharField(max_length=100, null=True, blank=False)
    date_of_sale = DateField(null=True, blank=False)
    status = CharField(max_length=42, null=True, blank=False)
    User = ForeignKey(Profile, on_delete=DO_NOTHING, null=True, blank=False)

    # _processed = models.BooleanField(default=False, editable=False)  # Temporary flag


class Order_Line(Model):
    product_price = IntegerField(default=0, null=True, blank=False)
    quantity = IntegerField(default=1, null=True, blank=False)
    Product = ForeignKey(Product, on_delete=DO_NOTHING, null=True, blank=False)
    Order = ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)

    def total_order_line_price(self):
        return self.product_price * self.quantity

    total_order_line_price.short_description = 'Total Price'


# Model pro objednávku
class Order(models.Model):
    total_cost = models.IntegerField(default=0, null=True, blank=False)  # Celková cena objednávky
    delivery_address = models.CharField(max_length=100, null=True, blank=False)  # Dodací adresa
    # user_address = models.CharField(max_length=100, null=True, blank=False)  # TODO: Adresa uživatele (pokud je jiná než dodací)
    date_of_sale = models.DateField(null=True, blank=False)  # Datum prodeje
    status = models.CharField(max_length=42, null=True, blank=False)  # Stav objednávky
    User = models.ForeignKey(Profile, on_delete=DO_NOTHING, null=True, blank=False)  # Uživatel, který vytvořil objednávku


# Model pro položky objednávky
class Order_Line(models.Model):
    product_price = models.IntegerField(default=0, null=True, blank=False)  # Cena produktu v objednávce
    quantity = models.IntegerField(default=0, null=True, blank=False)  # Množství produktu v objednávce
    Product = models.ForeignKey(Product, on_delete=DO_NOTHING, null=True, blank=False)  # Produkt v objednávce
    Order = models.ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)  # Objednávka, do které položka patří


# Model pro platbu
class Payment(models.Model):
    # sum = models.IntegerField(default=0, null=True, blank=False)  # TODO: Suma platby (je-li potřebná)
    # User = models.ForeignKey(Profile, on_delete=DO_NOTHING, null=True, blank=False)  # TODO: Uživatel, který provedl platbu
    Order = models.ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)  # Objednávka, ke které platba patří
    date_of_payment = models.DateTimeField(null=True, blank=False)  # Datum a čas platby
