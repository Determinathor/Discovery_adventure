from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, OneToOneField, CASCADE, TextField, DateField, EmailField, CharField, IntegerField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    # email = EmailField(unique=True)
    address = CharField(max_length=80, null=True, blank=False)
    phone_number = IntegerField(default=0, unique=True, null=True, blank=False)
    city = CharField(max_length=42, null=True, blank=False)

    def __repr__(self):
        return f"Profile(user={self.user})"

    def __str__(self):
        return f"{self.user.email}"




