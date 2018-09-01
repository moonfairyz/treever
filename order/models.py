from django.db import models

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