from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user}'s Cart"
