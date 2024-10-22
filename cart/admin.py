from django.contrib import admin

# Register your models here.
from .models import CartModel


@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "cart_data",
    )
