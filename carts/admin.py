from django.contrib import admin
from .models import Cart, CartItem
from django.urls import path, include

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)