from django.db import models
from django.contrib.auth.models import User

# Customer model
class Customer(models.Model):
    # User can only have one Customer | Customer can only have one User
    user =  models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    # How each instance will show up in the admin panel
    def __str__(self):
        return self.name
    
# Product model
class Product(models.Model):
    name =  models.CharField(max_length=200)
    price = models.FloatField()
    # Define if the product needs to be shipped (digital prodcuts do not need to be shipped)
    # By default every product will be a physical item
    digital = models.BooleanField(default=False, null=True, blank=True)

    image = models.ImageField(null=True, blank=True)

    # How each instance will show up in the admin panel
    def __str__(self):
        return self.name
    
    # Handling error if no product image is set
    @property # property decorator: lets you access this as an attribut rather than a method
    def imageURL(self):
        try:
            url = self.image.url   
        except:    
            url = ''
        return url
    
# Order model
class Order(models.Model):
    # Customers can have multiple orders
    # If customer is deleted, order is kept, customer is set to NULL
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # Open cart = False | Closed cart = True
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    # How each instance will show up in the admin panel
    def __str__(self):
        # Can only return string values here
        return str(self.id)
    
# Order item model (Item within Cart)
class OrderItem(models.Model):
    # Single product can be in multiple OrderItem
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # Single order can have multiple OrderItems
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # How each instance will show up in the admin panel
    def __str__(self):
        return self.product.name

# Order Shipping model (Item within Cart)
class ShippingAddress(models.Model):
    # Specific to one customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    # Specific to one order
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)  
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    # How each instance will show up in the admin panel
    def __str__(self):
        return self.address    



