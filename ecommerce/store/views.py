from django.shortcuts import render
from .models import *

# Create your views here.
def store(request):
     # Get queryset
     products = Product.objects.all()
     context = {'products': products}
     return render(request, 'store/store.html', context)

def cart(request):

     # Check if user is authenticated
     if request.user.is_authenticated:
          customer = request.user.customer
          # Get all open orders (complete=False) from customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
     else:
          items = []
          # Empty cart for non-logged in users
          order = {'get_cart_total': 0, 'get_cart_items': 0}

     context = {'items': items, 'order': order}
     return render(request, 'store/cart.html', context)

def checkout(request):

      # Check if user is authenticated
     if request.user.is_authenticated:
          customer = request.user.customer
          # Get all open orders (complete=False) from customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
     else:
          items = []
          # Empty cart for non-logged in users
          order = {'get_cart_total': 0, 'get_cart_items': 0}

     context = {'items': items, 'order': order}
     return render(request, 'store/checkout.html', context)