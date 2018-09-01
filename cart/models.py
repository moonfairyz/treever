from django.db import models
from django.contrib.auth.models import User

from shop.models import Product, Service

class Cart(models.Model):
	'''
	The Shopping cart
	'''
	cart_id = models.CharField(max_length=250, blank=True)
	date_added = models.DateField(auto_now_add=True)
	class Meta:
		db_table = 'Cart'
		ordering = ['date_added']

	def __str__(self):
		return self.cart_id

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	active = models.BooleanField(default=True)
	class Meta:
		db_table = 'CartItem'

	def sub_total(self):
		return self.product.price * self.quantity

	def __str__(self):
		return self.product.name
	
	
class UserProfile(models.Model):
	'''
	A customer profile
	'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=250, blank=True)
	city = models.CharField(max_length=250, blank=True)
	postcode = models.CharField(max_length=10, blank=True)
	country = models.CharField(max_length=200, blank=True)
	