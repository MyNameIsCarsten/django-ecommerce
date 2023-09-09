from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
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

@csrf_exempt
def payment_completed_view(request):
     context = request.POST
     return render(request, 'store/payment-completed.html', {'context': context})

@csrf_exempt
def payment_failed_view(request):
     return render(request, 'store/payment-failed.html')


import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ARRcoBGpGczOv-ojhkx98m-WsCKVtFjQ-hclh2BnjFAyciyvXSmpPIDDhoB1G6-XOo-g0cmuuMeN9Ta_",
  "client_secret": "EH27rqxfWZsQ4mRK_-DCctk_9Dy18YezfaawMihUDByqzG449vLxv0imsgRqcmDfgB2TDco6_gyalUNH" })

def create_payment(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": f'{order.get_cart_total}',  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        order.complete = True
        order.save()
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    
    else:
        return render(request, 'store/payment_failed.html')
    
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'store/payment_success.html')
    else:
        return render(request, 'store/payment_failed.html')

def payment_checkout(request):
    return render(request, 'store/checkout.html')