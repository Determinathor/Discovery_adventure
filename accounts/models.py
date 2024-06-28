from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model, OneToOneField, CASCADE, TextField, DateField, EmailField


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    email = EmailField(unique=True)

    def __repr__(self):
        return f"Profile(user={self.user})"

    def __str__(self):
        return f"{self.user}"
