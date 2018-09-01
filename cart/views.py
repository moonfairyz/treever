import braintree

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from order.models import Order, OrderItem, UserProfile
from shop.models import Product, Service
from .models import Cart, CartItem
from order.forms import ProfileForm



def _cart_id(request):
	'''
	get or create a cart id
	'''
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart


def add_cart(request, product_id):
	'''
	Adds a product to the cart
	'''
	
	product = Product.objects.get(id=product_id)
	cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
	cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart, active=True)
	if not created:
		cart_item.quantity += 1
		cart_item.save()
		
	return redirect('cart:cart_detail')

@login_required
def get_address(request):
	'''
	Get the shipping address.
	
	We will save it as the user's profile so that he needs not type it again the next time.
	Braintree does not directly collect this information. We have to collect it with our own
	form. 
	'''
	profile, _ = UserProfile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect(reverse('cart:checkout'))
		else:
			print(form)
			print(form.errors)
	else:
		form = ProfileForm(instance=profile)
		
	return render(request, 'profile.html', {'form': form})

def checkout(request):
	'''
	The actual checkout page
	'''
	gateway = braintree.BraintreeGateway(
	    braintree.Configuration(
	        environment=settings.BRAINTRRE_ENVIRONMENT,
	        merchant_id=settings.BRAINTREE_MERCHANT_ID,
	        public_key=settings.BRAINTREE_PUBLIC_KEY,
	        private_key=settings.BRAINTREE_PRIVATE_KEY
	    )
	)

	if request.method == 'GET':
	
		client_token = gateway.client_token.generate()
		return render(request, 'checkout.html', {'client_token': client_token})

	else:
		result = gateway.transaction.sale({
			'amount': request.POST['amount'],
			'payment_method_nonce': request.POST['payment_method_nonce'],
			'options': {
				"submit_for_settlement": True
			}
		})
		
		if result.is_success or  result.transaction:
			return HttpResponse('Done')
	
		return HttpResponse('Failed')
	
def cart_detail(request, total=0, counter=0, cart_items=None):
	'''
	Display a cart
	'''
	
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		for cart_item in cart_items:
			# total += (cart_item.product.price * cart_item.quantity)
			total = 0
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		raise Http404

	
	stripe_total = int(total * 100)
	description = 'Perfect Cushion Shop - New Order'
	
	#request.session['braintree_client_token'] = braintree.ClientToken.generate()
	return render(request, 'cart.html', dict(cart_items=cart_items, total=total, 
											counter=counter, stripe_total=stripe_total, description=description))


def cart_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -= 1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart:cart_detail')


def full_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart:cart_detail')


def sendEmail(order_id):
	transaction = Order.objects.get(id=order_id)
	order_items = OrderItem.objects.filter(order=transaction)
	try:
		'''Sending the order to the customer'''
		subject = "Perfect Cushion Store - New Order #{}".format(transaction.id)
		to = ['{}'.format(transaction.emailAddress)]
		from_email = "orders@perfectcushionstore.com"
		order_information = {
		'transaction' : transaction,
		'order_items' : order_items
		}
		message = get_template('email/email.html').render(order_information)
		msg = EmailMessage(subject, message, to=to, from_email=from_email)
		msg.content_subtype = 'html'
		msg.send()
	except IOError as e:
		return e
