from itertools import product
from multiprocessing.sharedctypes import Value
from django.db import connections
from apiserver.models import *
from django.http import JsonResponse, HttpResponse
import json, random, string, re
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

def tokenCreation():
    """
    Creation of unique token assigned to user
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k = 16))

def tokenIn(token):
    """
    Token exist or not
    """
    try:
        _token = users.objects.filter(token = token)
    except users.DoesNotExist:
        _token = None
    
    if _token:
        return True
    else:
        return False

def checkFilledFields(rbody, required):
    """
    Check, if user filled every required field
    """
    for element in required:
        if element not in rbody:
            return False
    
    return True

def formatEmail(email):
    """
    Check if email is in correct format
    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):
        return True
    else:
        return False

def uptime(request):
    """
    Uptime of database (testing request)
    """
    database = connections['default'].cursor()
    database.execute("SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime;")
    return JsonResponse({"pgsql": { " uptime": str(database.fetchone()[0]).replace(',', '') }})

"""
------------- USER REQUESTS -----------
"""
@csrf_exempt
def createUser(request):
    """
    Create user
    """
    rbody = json.loads(request.body.decode('utf-8'))
    required = ['username', 'password']
    token = True

    if not checkFilledFields(rbody, required):
        return HttpResponse(status = 400)
   
    try:
        user = users.objects.filter(username = rbody['username'])
    except users.DoesNotExist:
        user = None
    
    if user:
        return HttpResponse(status = 409)
    else:
        while token:
            random_token = tokenCreation()
            token = tokenIn(random_token)

        _user = users(username = rbody['username'], password = rbody['password'], token = random_token)
        _user.save()

    return HttpResponse(status = 201)

@csrf_exempt
def updateUser(request):
    """
    Update user
    """
    rbody = json.loads(request.body.decode('utf-8'))
    token = request.META.get('HTTP_TOKEN')

    if not token:
        return HttpResponse(status = 400)
    
    if "email" in rbody and not formatEmail(rbody['email']):
        return HttpResponse(status = 400)
    
    try:
        user = users.objects.filter(token = token)
    except users.DoesNotExist:
        user = None

    if user:

        if rbody.get('username') is not None:
            if users.objects.filter(username = rbody['username']).exists():
                return HttpResponse(status = 409)
        
        users.objects.filter(token = token).update(**rbody)         
        return HttpResponse(status = 200)

    else:
        return HttpResponse(status = 404)

@csrf_exempt
def deleteUser(request):
    """
    Delete user
    """
    token = request.META.get('HTTP_TOKEN')

    if not token: 
        return HttpResponse(status = 400)

    try:
        user = users.objects.filter(token = token)
    except users.DoesNotExist:
        user = None

    if user: 
        users.objects.filter(token = token).delete()
        return HttpResponse(status = 204)
    else:
        return HttpResponse(status = 404)

@csrf_exempt
def loginUser(request):
    """
    User login
    """
    rbody = json.loads(request.body.decode('utf-8'))
    required = ['username', 'password']

    if not checkFilledFields(rbody, required):
        return HttpResponse(status = 400)

    try:
        user = users.objects.get(username = rbody['username'], password = rbody['password'])
    except users.DoesNotExist:
        user = None
    
    if user:
        return JsonResponse({"token" : user.token, 
                            "username" : user.username, 
                            "password" : user.password}, status = 200, safe = False)
    else:
        return HttpResponse(status = 404)
    

@csrf_exempt
def getInfoUser(request):
    """
    Info user
    """
    id_user = request.GET.get('id', None)
    response = {}

    try:
        user = users.objects.get(id = id_user)
    except users.DoesNotExist:
        user = None

    if user:
        _user = {
                "firstname" : user.firstname,
                "lastname" : user.lastname,
                "username" : user.username,
                "password" : user.password,
                "email" : user.email,
                "phonenumber" : user.phonenumber,
                "token" : user.token
                }
        
        response.update(_user)
        return JsonResponse(response, status = 200, safe = False)
    
    else:
        return HttpResponse(status = 404)

"""
------------- DELIVERY METHODS REQUESTS -----------
"""
@csrf_exempt
def getDeliveryMethods(request):
    """
    Get all delivery methods
    """
    deliverymethods  = delivery_methods.objects.all()
    arr = []

    for deliverymethod in deliverymethods:
        arr.append(
            {"id" : deliverymethod.id,
            "deliverymethod" : deliverymethod.deliverymethod
            }
        )
    
    return JsonResponse(arr, status = 200, safe = False)

@csrf_exempt
def getDeliveryMethod(request):
    """
    Get delivery method
    """
    id_delivery_method = request.GET.get('id', None)
    response = {}
    
    try:
        deliverymethod = delivery_methods.objects.get(id = id_delivery_method)
    except delivery_methods.DoesNotExist:
        deliverymethod = None
    
    if deliverymethod:
        _deliverymethod = {
            "id" : deliverymethod.id,
            "deliverymethod" : deliverymethod.deliverymethod                
        }

        response.update(_deliverymethod)
        return JsonResponse(response, status = 200, safe = False)
        
    else:
        return HttpResponse(status = 404)

"""
------------- PAYMENT METHODS REQUESTS -----------
"""
@csrf_exempt
def getPaymentMethods(request):
    """
    Get all payment methods
    """
    paymentmethods  = payment_methods.objects.all()
    arr = []

    for paymentmethod in paymentmethods:
        arr.append(
            {"id" : paymentmethod.id,
            "paymentmethod" : paymentmethod.paymentmethod
            }
        )
    
    return JsonResponse(arr, status = 200, safe = False)

@csrf_exempt
def getPaymentMethod(request):
    """
    Get payment method
    """
    id_payment_method = request.GET.get('id', None)
    response = {}
    
    try:
        paymentmethod = payment_methods.objects.get(id = id_payment_method)
    except payment_methods.DoesNotExist:
        paymentmethod = None
    
    if paymentmethod:
        _paymentmethod = {
            "id" : paymentmethod.id,
            "deliverymethod" : paymentmethod.paymentmethod                
        }

        response.update(_paymentmethod)
        return JsonResponse(response, status = 200, safe = False)
        
    else:
        return HttpResponse(status = 404)

"""
------------- PRODUCT CATEGORY REQUESTS -----------
"""
@csrf_exempt
def getProductCategories(request):
    """
    Get all product categories
    """
    productcategories  = product_categories.objects.all()
    arr = []

    for productcategory in productcategories:
        arr.append(
            {"id" : productcategory.id,
            "categoryname" : productcategory.categoryname
            }
        )
    
    return JsonResponse(arr, status = 200, safe = False)

@csrf_exempt
def getProductCategory(request):
    """
    Get product category
    """
    id_product_category = request.GET.get('id', None)
    response = {}
    
    try:
        productcategory = product_categories.objects.get(id = id_product_category)
    except product_categories.DoesNotExist:
        productcategory = None
    
    if productcategory:
        _productcategory = {
            "id" : productcategory.id,
            "deliverymethod" : productcategory.categoryname                
        }

        response.update(_productcategory)
        return JsonResponse(response, status = 200, safe = False)
        
    else:
        return HttpResponse(status = 404)

"""
------------- VOUCHER REQUESTS -----------
"""
@csrf_exempt
def getVoucher(request):
    """
    Get voucher
    """
    id_voucher = request.GET.get('id', None)
    response = {}
    
    try:
        voucher = vouchers.objects.get(id = id_voucher)
    except vouchers.DoesNotExist:
        voucher = None
    
    if voucher:
        _voucher = {
            "id" : voucher.id,
            "code" : voucher.code,
            "discount" : voucher.discount,
            "isactive" : voucher.isactive               
        }

        response.update(_voucher)
        return JsonResponse(response, status = 200, safe = False)
        
    else:
        return HttpResponse(status = 404)

"""
------------- PRODUCTS REQUESTS -----------
"""
@csrf_exempt
def getProducts(request):
    """
    Get products
    """
    _products  = products.objects.all()
    arr = []

    for product in _products:
        arr.append(
            {"id" : product.id,
            "title" : product.title,
            "description" : product.description,
            "imagepath" : product.imagepath,
            "price" : product.price,
            "productcategory" : product.id_productcategory_id
            }
        )
    
    return JsonResponse(arr, status = 200, safe = False)

@csrf_exempt
def getProductsByCategory(request):
    """
    Get products by category
    """
    id_productcategory_id = request.GET.get('id_productcategory_id', None)
    arr = []
    
    try:
        _products = products.objects.filter(id_productcategory_id = id_productcategory_id)
    except products.DoesNotExist:
        _products = None
    
    if _products:
        
        for product in _products:
            arr.append(
            {
            "id" : product.id,
            "title" : product.title,
            "description" : product.description,
            "imagepath" : product.imagepath,
            "price" : product.price,
            "productcategory" : product.id_productcategory_id
            })

        return JsonResponse(arr, status = 200, safe = False)
        
    else:
        return HttpResponse(status = 204)


@csrf_exempt
def getProduct(request):
    """
    Get product by id
    """
    id_product = request.GET.get('id', None)
    response = {}
    
    try:
        product = products.objects.get(id = id_product)
    except products.DoesNotExist:
        product = None
    
    if product:
        
        _product = {
            "id" : product.id,
            "title" : product.title,
            "description" : product.description,
            "imagepath" : product.imagepath,
            "price" : product.price,
            "productcategory" : product.id_productcategory_id
            }
        
        response.update(_product)
        return JsonResponse(_product, status = 200, safe = False)
        
    else:
        return HttpResponse(status = 204)

@csrf_exempt
def createProduct(request):
    """
    Create product
    """
    rbody = json.loads(request.body.decode('utf-8'))
    required = ['title', 'description', 'imagepath', 'price', 'id_productcategory_id']

    if not checkFilledFields(rbody, required):
        return HttpResponse(status = 400)
   
    try:
        product = products.objects.filter(title = rbody['title'])
    except products.DoesNotExist:
        product = None
    
    if product:
        return HttpResponse(status = 409)
    else:
        _product = products(title = rbody['title'], description = rbody['description'],
                        imagepath = rbody['imagepath'], price = rbody['price'], 
                        id_productcategory_id = rbody['id_productcategory_id'])
        _product.save()

    return HttpResponse(status = 201)

@csrf_exempt
def updateProduct(request):
    """
    Update product by id
    """
    rbody = json.loads(request.body.decode('utf-8'))
    id_product = request.GET.get('id', None)

    try:
        product = products.objects.filter(id = id_product)
    except products.DoesNotExist:
        product = None

    if product:

        products.objects.filter(id = id_product).update(**rbody)         
        return HttpResponse(status = 200)

    else:
        return HttpResponse(status = 404)

@csrf_exempt
def deleteProduct(request):
    """
    Delete product by id
    """
    id_product = request.GET.get('id', None)

    try:
        product = products.objects.filter(id = id_product)
    except products.DoesNotExist:
        product = None

    if product: 
        products.objects.filter(id = id_product).delete()
        return HttpResponse(status = 204)
    else:
        return HttpResponse(status = 404)

# orders requests
def getUsersOrders(request, id_user):
    """
    Get all orders with user id
    """
    _orders = orders.objects.filter(id_user_id = id_user)
    _orders = _orders.values('id', 'firstname', 'lastname', 'email', 'phonenumber', 'adress', 'city', 'zipcode',
                             'cardnumber', 'cardcsv', 'finished', 'created', 'id_deliverymethod', 'id_paymentmethod',
                             'id_user', 'id_voucher')
    return JsonResponse(list(_orders), safe=False, status=200)

def getSpecificOrder(request, id_order):
    """
    Get specific user's order
    """

    _order = orders.objects.get(id=id_order)
    return JsonResponse(model_to_dict(_order), safe=False, status=200)
