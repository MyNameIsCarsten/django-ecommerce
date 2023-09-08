from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request):
     data = cartData(request)

     cartItems = data['cartItems']

     # Get queryset
     products = Product.objects.all()
     context = {'products': products, 'cartItems': cartItems}
     return render(request, 'store/store.html', context)

def cart(request):

     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items': items, 'order': order, 'cartItems': cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):

     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items': items, 'order': order, 'cartItems': cartItems}
     return render(request, 'store/checkout.html', context)

def updateItem (request):
     data = json.loads(request.body) # access fetch request body
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('Product:', productId)
     
     customer = request.user.customer # logged in customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     # If the orderItem exists: we change it, if not: we create it
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == 'add':
          orderItem.quantity += 1
     elif action == 'remove':
          orderItem.quantity -= 1
     
     orderItem.save() # save to database

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)

def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     #print('Data:', request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)

     else:
          customer, order = guestOrder(request, data)

     total = float(data['form']['total']) # access userFormData
     order.transaction_id = transaction_id

     if total == order.get_cart_total: # check if total is same as cart_total
          order.complete = True
     order.save()

     if order.shipping == True:
          ShippingAddress.objects.create(
               customer=customer,
               order=order,
               address=data['shipping']['address'],
               city=data['shipping']['city'],
               state=data['shipping']['state'],
               zipcode=data['shipping']['zipcode'],
          )

     return JsonResponse('Payment submitted', safe=False)