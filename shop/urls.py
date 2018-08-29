from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
	
	path('profile/<username>/', views.MyProfile, name='MyProfile'),
	path('create_product/', views.CreateProduct, name='Create_Product'),
	path('edit_product/<slug:product_slug>/', views.EditProduct, name='Edit_Product'),
	path('delete_product/<slug:product_slug>/', views.DeleteProduct, name='Delete_Product'),
	path('allservices/', views.AllService, name='AllService'),
	path('allservices/<slug:service_slug>/', views.ServiceDetail, name='ServiceDetail'),
	path('allproducts/', views.AllProduct, name='AllProduct'),
	path('allproducts/<slug:product_slug>/', views.product_detail, name='ProductDetail'),

]



