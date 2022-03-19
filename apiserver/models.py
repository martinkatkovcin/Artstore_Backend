from django.db import models
from django.forms import BooleanField

class product_categories(models.Model):
    class Meta:
        db_table = 'product_categories'
        
    id = models.AutoField(primary_key = True)
    categoryname = models.CharField(max_length = 50)

class delivery_methods(models.Model):
    class Meta:
        db_table = 'delivery_methods'

    id = models.AutoField(primary_key = True)
    deliverymethod = models.CharField(max_length = 50)

class vouchers(models.Model):
    class Meta:
        db_table = 'vouchers' 

    id = models.AutoField(primary_key = True)
    code = models.CharField(max_length = 50)
    discount = models.FloatField()
    isactive = models.BooleanField()

class payment_methods(models.Model):
    class Meta:
        db_table = 'payment_methods'    
        
    id = models.AutoField(primary_key = True)
    paymentmethod = models.CharField(max_length = 50)

class users(models.Model):
    class Meta:
        db_table = 'users'   
        
    id = models.AutoField(primary_key = True)
    firstname = models.CharField(max_length = 50, blank = True, null = True)
    lastName = models.CharField(max_length = 50, blank = True, null = True)
    username = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254, unique = True, blank = True, null = True)
    phonenumber = models.CharField(max_length = 50, blank = True, null = True)
    token = models.TextField()

class products(models.Model):
    class Meta:
        db_table = 'products' 
        
    id = models.AutoField(primary_key = True)
    id_productcategory = models.ForeignKey(product_categories, on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 255)
    imagepath = models.CharField(max_length = 255)
    price = models.FloatField()
    
class orders(models.Model):
    class Meta:
        db_table = 'orders'   
    
    id = models.AutoField(primary_key = True)
    id_user = models.ForeignKey(users, on_delete = models.CASCADE)
    id_paymentmethod = models.ForeignKey(payment_methods, on_delete = models.CASCADE)
    id_deliverymethod = models.ForeignKey(delivery_methods, on_delete = models.CASCADE)
    id_voucher = models.ForeignKey(vouchers, on_delete = models.CASCADE)
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254)
    phonenumber = models.CharField(max_length = 50)
    adress = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    zipcode = models.IntegerField()
    cardnumber = models.IntegerField()
    cardexpirationdate = models.CharField(max_length = 50)
    cardcsv = models.IntegerField()
    finished = models.BooleanField()
    created = models.DateTimeField(auto_now_add = True)

class order_items(models.Model):
    class Meta:
        db_table = 'order_items'  
         
    id = models.AutoField(primary_key = True)
    id_product= models.ForeignKey(products, on_delete = models.CASCADE)
    id_order = models.ForeignKey(orders, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)