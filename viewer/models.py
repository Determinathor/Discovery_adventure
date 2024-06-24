from datetime import date

from django.db.models import *  #(Model, CharField, ForeignKey, DO_NOTHING,

# Create your models here.

class Role(Model):
    role_name = CharField(max_length=42, null=False, blank=False)
class User(Model):
    first_name = CharField(max_length=42, null=False, blank=False)
    last_name = CharField(max_length=42, null=False, blank=False)
    email = CharField(max_length=128, unique=True, null=False, blank=False)
    password = CharField(max_length=80, null=False, blank=False)
    address = CharField(max_length=80, null=False, blank=False)
    phone_number = IntegerField(unique=True, null=False, blank=False)
    city = CharField(max_length=42, null=False, blank=False)
    role = ForeignKey(Role, on_delete=CASCADE, null=False, blank=False)

class Product(Model):


class Product_Category(Model):
    pass

class Category(Model):
    pass
class Order(Model):
    pass

class Order_Lines(Model):
    pass

class Manufacturer(Model):
    pass

class Cart(Model):
    pass

class Cart_Products(Model):
    pass
class Payment(Model):
    pass



