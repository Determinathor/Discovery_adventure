from datetime import date

from django.db.models import *  #(Model, CharField, ForeignKey, DO_NOTHING,

# Create your models here.


class Role(Model):
    role_name = CharField(max_length=42, null=True, blank=False)


class User(Model):
    first_name = CharField(max_length=42, null=True, blank=False)
    last_name = CharField(max_length=42, null=True, blank=False)
    email = CharField(max_length=128, unique=True, null=True, blank=False)
    password = CharField(max_length=80, null=True, blank=False)
    address = CharField(max_length=80, null=True, blank=False)
    phone_number = IntegerField(default=0, unique=True, null=True, blank=False)
    city = CharField(max_length=42, null=True, blank=False)
    role = ForeignKey(Role, on_delete=CASCADE, null=True, blank=False)


class Manufacturer(Model):
    name = CharField(max_length=80, null=True, blank=False)


class Product(Model):
    title = CharField(max_length=100, null=True, blank=False)
    description = CharField(max_length=500, null=True, blank=False)
    thumbnail = CharField(max_length=500, null=True, blank=False)
    price = IntegerField(default=0, null=True, blank=False)
    product_type = CharField(max_length=42, null=True, blank=False)
    stock = IntegerField(default=0, null=True, blank=False)
    manufacturer = ForeignKey(Manufacturer,on_delete=DO_NOTHING, null=True, blank=False)


class Cart(Model):
    quantity = IntegerField(default=0, null=True, blank=False)
    Product = ManyToManyField(Product, related_name='cart')



class Category(Model):
    name = CharField(max_length=42, null=True, blank=False)
    Product = ManyToManyField(Product, related_name='category')



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




