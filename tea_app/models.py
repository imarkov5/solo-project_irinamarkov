from django.db import models
from log_and_reg.models import User
from decimal import Decimal



class Product(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Order(models.Model):
    user = models.ForeignKey(User, related_name="has_ordered", on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name="item_in_order", blank=True, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="item", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

# class ShippingInfo(models.Model):
#     user = models.ForeignKey(User, related_name="shipping_info", on_delete=models.CASCADE)
#     order = models.ForeignKey(User, related_name="shipping_info", on_delete=models.CASCADE)
#     address = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=45)
#     zip = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True) 
