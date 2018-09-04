from django.contrib import admin
from .models import Order, OrderItem, UserProfile

class OrderItemAdmin(admin.TabularInline):
	model = OrderItem
	fieldsets = [
	('Product',{'fields':['product'],}),
	('Quantity',{'fields':['quantity'],}),
	('Price',{'fields':['price'],}),
	]
	readonly_fields = ['product','quantity','price']
	can_delete= False
	max_num = 0
	template = 'admin/order/tabular.html'


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','address','city','postcode','country')
	

admin.site.register(UserProfile, ProfileAdmin)