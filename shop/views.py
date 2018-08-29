from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Service, Product, Profile
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .forms import SignUpForm

def Home(request):
	return render(request, 'home.html',{})

def AllService(request):
	services = Service.objects.filter(available=True)
	return render(request, 'shop/allservices.html', {'services':services})

@login_required(login_url="/")
def all_products(request):
	products = Product.objects.filter(available=True)
	return render(request, 'shop/allproducts.html', {'products':products})

@login_required(login_url="/")
def product_detail(request, product_slug):
	product = get_object_or_404(Product, slug=product_slug)
	return render(request, 'shop/product.html', {'product':product})

@login_required(login_url="/")
def ServiceDetail(request, service_slug):
	try:
		service = Service.objects.get(slug=service_slug)
	except Exception as e:
		raise e
	return render(request, 'shop/service.html', {'service':service})

#@login_required(login_url="/")
def CreateProduct(request):
	error = ''
	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			product = product_form.save(commit=False)
			product.user = request.user
			product.save()
			products = Product.objects.filter(user=request.user)
			return render(request, 'shop/allproducts.html', {'products':products})
		else:
			error = "Data is not valid"
	product_form = ProductForm()
	return render(request, 'shop/create_product.html', {'product_form': product_form, 'error': error})

@login_required(login_url="/")
def EditProduct(request, product_slug):
	try:
		product = Product.objects.get(slug=product_slug)
		error = ''
		if request.method == 'POST':
			product_form = ProductForm(request.POST, request.FILES, instance=product)
			if product_form.is_valid():
				product_form.save()
				return redirect('shop:all-products')
			else:
				error = "Data is not valid"
		else:
			product_form = ProductForm(instance=product)
		return render(request, 'shop/edit_product.html', {'product_form':product_form, 'error':error})
	except Product.DoesNotExist:
		return redirect('shop:all-products')

@login_required(login_url="/")
def DeleteProduct(request, product_slug):
	product = Product.objects.get(slug=product_slug)
	if request.method == 'POST':
		product.delete()
		return redirect('shop:all-products')
	return render(request, 'shop/delete_product.html', {'product': product})

@login_required(login_url="/")
def MyProfile(request, username):
	profile = Profile.objects.get(user__username=username)
	return render(request, 'accounts/profile.html', {'profile':profile})

def signupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			customer_group = Group.objects.get(name='Customer')
			customer_group.user_set.add(signup_user)
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form':form})

def signinView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('shop:Create_Product')
			else:
				return redirect('signup')
	else:
		form = AuthenticationForm()
	return render(request,'accounts/signin.html', {'form':form })

def signoutView(request):
	logout(request)
	return redirect('signin')
