import braintree

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

from order.models import Order, OrderItem
from shop.models import Product, Service
from .models import Cart, CartItem
from django.http.response import Http404



def _cart_id(request):
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


def checkout(request):
	pass

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

	gateway = braintree.BraintreeGateway(
	    braintree.Configuration(
	        environment=settings.BRAINTRRE_ENVIRONMENT,
	        merchant_id=settings.BRAINTREE_MERCHANT_ID,
	        public_key=settings.BRAINTREE_PUBLIC_KEY,
	        private_key=settings.BRAINTREE_PRIVATE_KEY
	    )
	)
	client_token = gateway.client_token.generate()
	
	stripe_total = int(total * 100)
	description = 'Perfect Cushion Shop - New Order'
	
	if request.method == 'POST':
		# print(request.POST)
		try:
			token = request.POST['stripeToken']
			email = request.POST['stripeEmail']
			billingName = request.POST['stripeBillingName']
			billingAddress1 = request.POST['stripeBillingAddressLine1']
			billingcity = request.POST['stripeBillingAddressCity']
			billingPostcode = request.POST['stripeBillingAddressZip']
			billingCountry = request.POST['stripeBillingAddressCountryCode']
			shippingName = request.POST['stripeShippingName']
			shippingAddress1 = request.POST['stripeShippingAddressLine1']
			shippingcity = request.POST['stripeShippingAddressCity']
			shippingPostcode = request.POST['stripeShippingAddressZip']
			shippingCountry = request.POST['stripeShippingAddressCountryCode']
			customer = stripe.Customer.create(
						email=email,
						source=token
				)
			
			charge = stripe.Charge.create(
						amount=stripe_total,
						currency="gbp",
						description=description,
						customer=customer.id
				)
			'''Creating the order'''
			try:
				order_details = Order.objects.create(
						token=token,
						total=total,
						emailAddress=email,
						billingName=billingName,
						billingAddress1=billingAddress1,
						billingCity=billingcity,
						billingPostcode=billingPostcode,
						billingCountry=billingCountry,
						shippingName=shippingName,
						shippingAddress1=shippingAddress1,
						shippingCity=shippingcity,
						shippingPostcode=shippingPostcode,
						shippingCountry=shippingCountry
					)
				order_details.save()
				for order_item in cart_items:
					oi = OrderItem.objects.create(
							product=order_item.product.name,
							quantity=order_item.quantity,
							price=order_item.product.price,
							order=order_details
						)
					oi.save()
					'''Reduce stock when order is placed or saved'''
					products = Product.objects.get(id=order_item.product.id)
					products.stock = int(order_item.product.stock - order_item.quantity)
					products.save()
					order_item.delete()
					'''The terminal will print this message when the order is saved'''
					print('The order has been created')
				try:  # email part start
					'''Calling the sendEmail function'''
					sendEmail(order_details.id)
					print('The order email has been sent to the customer.')
				except IOError as e:
					return e
				return redirect('order:thanks', order_details.id)
			except ObjectDoesNotExist:
				pass
		except :
			import traceback
			traceback.print_exc()
			return False, e
		
	#request.session['braintree_client_token'] = braintree.ClientToken.generate()
	return render(request, 'cart.html', dict(cart_items=cart_items, total=total, client_token=client_token,
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
