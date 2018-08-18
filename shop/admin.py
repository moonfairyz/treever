from django.contrib import admin
from .models import Service, Product, Profile

class ServiceAdmin(admin.ModelAdmin):
	list_display = ['title','description','price','available','created']
	list_editable = ['price','available']
	prepopulated_fields = {'slug':('title',)}
	list_per_page = 20
admin.site.register(Service,ServiceAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ['name','service','latitude','longitude','image','user','created','updated','available']
	list_editable = ['available']
	prepopulated_fields = {'slug':('name',)}
	list_per_page = 20
admin.site.register(Product,ProductAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user','about']
admin.site.register(Profile,ProfileAdmin)