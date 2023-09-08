import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)
    items = []
    # Empty cart for non-logged in users
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
    cartItems = order['get_cart_items']

    # Loop through cart, i will be productId
    for i in cart:
        # Use try block to prevent items in cart that may been removed
        try:
            cartItems += cart[i]['quantity'] 

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            # since the user is not logged in, we cannot query for their cart
            # for each item, we will thus create an item entry in items dictionary
            # this will help us display all items with their cart
            item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL': product.imageURL
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
            }
            items.append(item)

            if product.digital == False:
                    order['shipping'] = True
        except:
            pass
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):
     # Check if user is authenticated
     if request.user.is_authenticated:
          customer = request.user.customer
          # Get all open orders (complete=False) from customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          cookieData = cookieCart(request)
          cartItems = cookieData['cartItems']
          order = cookieData['order']
          items = cookieData['items']
     return {'items': items, 'order': order, 'cartItems': cartItems}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    # Create a new customer (if email is not found in database)
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    # Create a new order for this customer
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    # Loop through items in cookies and add them as orderItems to the order
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem =OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order