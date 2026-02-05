from django.contrib import admin
from .models import Cart, CartItem
from django.urls import path, include

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'color', 'size', 'quantity', 'is_active')
    readonly_fields = ('product',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    inlines = [CartItemInline]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'quantity', 'is_active')
    list_filter = ('is_active', 'cart')
    search_fields = ('product__product_name', 'color', 'size')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)