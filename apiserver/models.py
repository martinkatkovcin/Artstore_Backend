from tkinter import CASCADE
from django.db import models
from django.forms import BooleanField
from sqlalchemy import false

class Product_categories(models.Model):
    class Meta:
        db_table = 'Product_categories'
        managed = false

    id = models.AutoField(primary_key = True)
    categoryName = models.CharField(max_length = 50)

class Delivery_methods(models.Model):
    class Meta:
        db_table = 'Delivery_methods'
        managed = false

    id = models.AutoField(primary_key = True)
    deliveryMethod = models.CharField(max_length = 50)

class Vouchers(models.Model):
    class Meta:
        db_table = 'Vouchers' 
        managed = false

    id = models.AutoField(primary_key = True)
    code = models.CharField(max_length = 50)
    discout = models.FloatField()
    isActive = models.BooleanField()

class Payment_methods(models.Model):
    class Meta:
        db_table = 'Payment_methods'    
        managed = false

    id = models.AutoField(primary_key = True)
    paymentMethod = models.CharField(max_length = 50)

class Users(models.Model):
    class Meta:
        db_table = 'Users'   
        managed = false

    id = models.AutoField(primary_key = True)
    firstName = models.CharField(max_length = 50, blank = True, null = True)
    lastName = models.CharField(max_length = 50, blank = True, null = True)
    username = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254, unique = True, blank = True, null = True)
    phoneNumber = models.CharField(max_length = 50, blank = True, null = True)
    token = models.TextField()

class Products(models.Model):
    class Meta:
        db_table = 'Products' 
        managed = false

    id = models.AutoField(primary_key = True)
    id_productCategory = models.ForeignKey(Product_categories, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 255)
    imagePath = models.CharField(max_length = 255)
    price = models.FloatField()
    
class Orders(models.Model):
    class Meta:
        db_table = 'Orders'   
        managed = false   
    id = models.AutoField(primary_key = True)
    id_user = models.ForeignKey(Users, on_delete = models.CASCADE)
    id_paymentMethod = models.ForeignKey(Payment_methods, on_delete = models.CASCADE)
    id_deliveryMethod = models.ForeignKey(Delivery_methods, on_delete = models.CASCADE)
    id_voucher = models.ForeignKey(Vouchers, on_delete = models.CASCADE)
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254)
    phoneNumber = models.CharField(max_length = 50)
    adress = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    zipCode = models.IntegerField()
    cardNumber = models.IntegerField()
    cardExpirationDate = models.CharField(max_length = 50)
    cardCSV = models.IntegerField()
    finished = models.BooleanField()
    created = models.DateTimeField(auto_now_add = True)

class Order_items(models.Model):
    class Meta:
        db_table = 'Order_items'  
        managed = false
        
    id = models.AutoField(primary_key = True)
    id_product= models.ForeignKey(Products, on_delete = models.CASCADE)
    id_order = models.ForeignKey(Orders, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)