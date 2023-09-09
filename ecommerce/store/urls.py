from django.urls import path
from store.views import payment_completed_view, payment_failed_view

from . import views

urlpatterns = [
    #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    
	path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    
	path('paypal-completed/', payment_completed_view, name='payment-completed'),
    path('paypal-failed/', payment_failed_view, name='payment_failed'),
    
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
]