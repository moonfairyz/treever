from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

class Service(models.Model):
	title = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='service', blank=True)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('title',)
		verbose_name = 'service'
		verbose_name_plural = 'services'

	def get_url(self):
		return reverse('shop:ServiceDetail', args=[self.slug])

	def __str__(self):
		return '{}'.format(self.title)

class Product(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, unique=True, blank=True)
	description = models.TextField(blank=True)
	service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to='product')
	latitude = models.DecimalField(max_digits=19, decimal_places=16)
	longitude = models.DecimalField(max_digits=19, decimal_places=16)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
	
	class Meta:
		ordering = ('name',)
		verbose_name = 'product'
		verbose_name_plural = 'products'

	def get_url(self):
		return reverse('shop:ProductDetail', args=[self.slug])

	def __str__(self):
		return '{}'.format(self.name)

	def _get_unique_slug(self):
		slug = slugify(self.name)
		unique_slug = slug
		num = 1
		while Product.objects.filter(slug=unique_slug).exists():
			unique_slug = '{}-{}'.format(slug, num)
			num += 1
		return unique_slug

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self._get_unique_slug()
		super().save(*args, **kwargs)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	about = models.CharField(max_length=100)
	address = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username

