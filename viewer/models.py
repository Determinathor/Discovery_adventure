from datetime import date

from django.db.models import *  #(Model, CharField, ForeignKey, DO_NOTHING,
from django.core.validators import MinValueValidator


# class Role(Model):
#     role_name = CharField(max_length=42, null=True, blank=False)


class User(Model):
    first_name = CharField(max_length=42, null=True, blank=False)
    last_name = CharField(max_length=42, null=True, blank=False)
    email = CharField(max_length=128, unique=True, null=True, blank=False)
    password = CharField(max_length=80, null=True, blank=False)
    address = CharField(max_length=80, null=True, blank=False)
    phone_number = IntegerField(default=0, unique=True, null=True, blank=False)
    city = CharField(max_length=42, null=True, blank=False)
    # role = ForeignKey(Role, on_delete=CASCADE, null=True, blank=False)

    class Meta:
        ordering = ['last_name', 'first_name', 'email', 'phone_number', 'city']


class Manufacturer(Model):
    name = CharField(max_length=80, null=True, blank=False)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f"<Manufacturer: {self.name}>"

    def __str__(self):
        return f"{self.name}"


class Product(Model):
    title = CharField(max_length=100, null=True, blank=False)
    description = CharField(max_length=500, null=True, blank=False)
    thumbnail = CharField(max_length=500, null=True, blank=False)
    price = IntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(1)])
    product_type = CharField(max_length=42, null=True, blank=False)
    stock = IntegerField(default=0, null=True, blank=False, validators=[MinValueValidator(0)])
    manufacturer = ForeignKey(Manufacturer,on_delete=DO_NOTHING, null=True, blank=False)

    class Meta:
        ordering = ['title', 'stock', 'price']

    def __str__(self):
        return f"{self.title}, in stock: {self.stock}, price: {self.price} CZK"

    def __repr__(self):
        return f"<Product: {self.title}, in stock: {self.stock}, price: {self.price} CZK>"


class Cart(Model):
    quantity = IntegerField(default=0, null=True, blank=False)
    Product = ManyToManyField(Product, related_name='cart')


class Category(Model):
    name = CharField(max_length=42, null=True, blank=False)
    Product = ManyToManyField(Product, related_name='category', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"


class Order(Model):
    total_cost = IntegerField(default=0, null=True, blank=False)
    delivery_address = CharField(max_length=100, null=True, blank=False)
    user_address = CharField(max_length=100, null=True, blank=False)
    date_of_sale = DateField(null=True, blank=False)
    status = CharField(max_length=42, null=True, blank=False)
    User = ForeignKey(User,on_delete=DO_NOTHING, null=True, blank=False)


class Order_Line(Model):
    product_price = IntegerField(default=0, null=True, blank=False)
    quantity = IntegerField(default=0, null=True, blank=False)
    Product = ForeignKey(Product, on_delete=DO_NOTHING, null=True, blank=False)
    Order = ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)


class Payment(Model):
    sum = IntegerField(default=0, null=True, blank=False)
    User = ForeignKey(User, on_delete=DO_NOTHING, null=True, blank=False)
    Order = ForeignKey(Order, on_delete=DO_NOTHING, null=True, blank=False)




