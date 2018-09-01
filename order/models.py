from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
	token = models.CharField(max_length=250, blank=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='GBP Order Total')
	created = models.DateTimeField(auto_now_add=True)


	class Meta:
		db_table = 'Order'
		ordering = ['-created']

	def __str__(self):
		return str(self.id)


class OrderItem(models.Model):
	product = models.CharField(max_length=250)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='GBP Price')
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	class Meta:
		db_table = 'OrderItem'

	def sub_total(self):
		return self.quantity * self.price

	def __str__(self):
		return self.product
	
	
	
class UserProfile(models.Model):
	'''
	A customer profile
	'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=250, blank=True)
	city = models.CharField(max_length=250, blank=True)
	postcode = models.CharField(max_length=10, blank=True)
	country = models.CharField(max_length=200, blank=True)
	
	