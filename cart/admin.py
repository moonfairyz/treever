from django.contrib import admin

from cart.models import CartItem
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','quantity', 'cart', 'active')
    
admin.site.register(CartItem, CartItemAdmin)