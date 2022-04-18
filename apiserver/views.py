from itertools import product
from multiprocessing.sharedctypes import Value
from django.db import connections
from django.http import FileResponse
from numpy import empty
from apiserver.models import *
from django.http import JsonResponse, HttpResponse
import json, random, string, re
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils import timezone
import base64, os, ctypes


def tokenCreation():
    """
    Creation of unique token assigned to user
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def tokenIn(token):
    """
    Token exist or not
    """
    try:
        _token = users.objects.filter(token=token)
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
    try:
        if rbody.get('username') == '' or rbody.get('password') == '':
            return False
    except:
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
        return HttpResponse(status=400)

    try:
        user = users.objects.filter(username=rbody['username'])
    except users.DoesNotExist:
        user = None

    if user:
        return HttpResponse(status=409)
    else:
        while token:
            random_token = tokenCreation()
            token = tokenIn(random_token)

        _user = users(username=rbody['username'], password=rbody['password'], token=random_token, isadmin=False)
        _user.save()

    return HttpResponse(status=201)


@csrf_exempt
def updateUser(request):
    """
    Update user
    """
    rbody = json.loads(request.body.decode('utf-8'))
    token = request.GET['token']

    if not token:
        return HttpResponse(status=400)

    if "email" in rbody and not formatEmail(rbody['email']):
        return HttpResponse(status=400)

    try:
        user = users.objects.filter(token=token)
    except users.DoesNotExist:
        user = None

    if user:

        if rbody.get('username') is not None:
            if users.objects.filter(username=rbody['username']).exists():
                return HttpResponse(status=409)

        users.objects.filter(token=token).update(**rbody)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def deleteUser(request):
    """
    Delete user
    """
    token = request.GET['token']

    if not token:
        return HttpResponse(status=400)

    try:
        user = users.objects.filter(token=token)
    except users.DoesNotExist:
        user = None

    if user:
        users.objects.filter(token=token).delete()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def loginUser(request):
    """
    User login
    """
    rbody = json.loads(request.body.decode('utf-8'))
    required = ['username', 'password']

    if not checkFilledFields(rbody, required):
        return HttpResponse(status=400)

    try:
        user = users.objects.get(username=rbody['username'], password=rbody['password'])
    except users.DoesNotExist:
        user = None

    if user:
        return JsonResponse({"token": user.token,
                             "username": user.username,
                             "password": user.password,
                             "isadmin": user.isadmin}
                            , status=200, safe=False)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def getInfoUser(request):
    """
    Info user
    """
    id_user = request.GET.get('token', None)
    response = {}

    try:
        user = users.objects.get(token=id_user)
    except users.DoesNotExist:
        user = None

    if user:
        _user = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "phonenumber": user.phonenumber,
            "token": user.token
        }

        response.update(_user)
        return JsonResponse(response, status=200, safe=False)

    else:
        return HttpResponse(status=404)


"""
------------- DELIVERY METHODS REQUESTS -----------
"""


@csrf_exempt
def getDeliveryMethods(request):
    """
    Get all delivery methods
    """
    deliverymethods = delivery_methods.objects.all()
    arr = []

    for deliverymethod in deliverymethods:
        arr.append(
            {"id": deliverymethod.id,
             "deliverymethod": deliverymethod.deliverymethod
             }
        )

    return JsonResponse(arr, status=200, safe=False)


"""
------------- PAYMENT METHODS REQUESTS -----------
"""


@csrf_exempt
def getPaymentMethods(request):
    """
    Get all payment methods
    """
    paymentmethods = payment_methods.objects.all()
    arr = []

    for paymentmethod in paymentmethods:
        arr.append(
            {"id": paymentmethod.id,
             "paymentmethod": paymentmethod.paymentmethod
             }
        )

    return JsonResponse(arr, status=200, safe=False)


"""
------------- PRODUCT CATEGORY REQUESTS -----------
"""


@csrf_exempt
def getProductCategories(request):
    """
    Get all product categories
    """
    productcategories = product_categories.objects.all()
    arr = []

    for productcategory in productcategories:
        arr.append(
            {"id": productcategory.id,
             "categoryname": productcategory.categoryname
             }
        )

    return JsonResponse(arr, status=200, safe=False)


"""
------------- VOUCHER REQUESTS -----------
"""


@csrf_exempt
def getVouchers(request):
    """
    Get voucher
    """
    given_voucher = request.GET.get('voucher', None)
    try:
        voucher = vouchers.objects.get(code=given_voucher)
        return JsonResponse({"discount": voucher.discount}, status=200, safe=False)
    except vouchers.DoesNotExist:
        return HttpResponse(status=404)


"""
------------- PRODUCTS REQUESTS -----------
"""


@csrf_exempt
def getProducts(request):
    """
    Get products
    """
    _products = products.objects.all()
    arr = []
    counter = 1

    for product in _products:
        arr.append(
            {"id": product.id,
             "title": product.title,
             "description": product.description,
             "image": str(product.image.tobytes()),
             "price": product.price,
             "productcategory": product.id_productcategory_id
             }
        )

        with open(os.path.join('Testimagesproducts', str(counter) + '.jpg'), 'wb') as f:
            f.write(product.image)

        counter = counter + 1

    return JsonResponse(arr, status=200, safe=False)


@csrf_exempt
def getProduct(request):
    """
    Get product by id
    """
    id_product = request.GET.get('id', None)
    response = {}

    try:
        product = products.objects.get(id=id_product)
    except products.DoesNotExist:
        product = None

    if product:

        _product = {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "image": str(product.image.tobytes()),
            "price": product.price,
            "productcategory": product.id_productcategory_id
        }

        # print(product.image, "\n")
        response.update(_product)
        """
        Saving to filesystem to test if we read image right
        """
        with open(os.path.join('TestimagesGET', "test.jpg"), 'wb') as f:
            f.write(product.image)

        return JsonResponse(_product, status=200, safe=False)

    else:
        return HttpResponse(status=204)


@csrf_exempt
def createProduct(request):
    """
    Create product
    """
    image = request.FILES['image'].read()
    basestr = base64.b64encode(image)
    imname = request.FILES['image'].name
    rbody = request.POST.dict()

    required = ['title', 'description', 'price', 'id_productcategory_id']

    if not checkFilledFields(rbody, required):
        return HttpResponse(status=400)

    try:
        product = products.objects.filter(title=rbody['title'])
    except products.DoesNotExist:
        product = None

    if product:
        return HttpResponse(status=409)
    else:
        if request.GET['isadmin'] == 'True':
            _product = products(title=rbody['title'], description=rbody['description'],
                                image=image, price=rbody['price'],
                                id_productcategory_id=rbody['id_productcategory_id'])
            _product.save()

            """
            Saving to filesystem to test if we read image right
            """
            with open(os.path.join('TestimagesPOST', imname), 'wb') as f:
                f.write(image)

            return HttpResponse(status=201)
        else:
            return HttpResponse(status=401)


@csrf_exempt
def updateProduct(request):
    """
    Update product by id
    """
    rbody = json.loads(request.body.decode('utf-8'))
    id_product = request.GET.get('id', None)

    try:
        product = products.objects.filter(id=id_product)
    except products.DoesNotExist:
        product = None

    if product:
        if request.GET['isadmin'] == 'True':
            products.objects.filter(id=id_product).update(**rbody)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def deleteProduct(request):
    """
    Delete product by id
    """
    id_product = request.GET.get('id', None)

    try:
        product = products.objects.filter(id=id_product)
    except products.DoesNotExist:
        product = None

    if product:
        if request.GET['isadmin'] == 'True':
            products.objects.filter(id=id_product).delete()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=404)


# orders requests
def createNewOrder(user_id):
    new_order = orders(firstname="", lastname="", email="", phonenumber="", adress="", city="", zipcode=0,
                       cardnumber=0, cardcsv=0, finished="False", id_deliverymethod_id=1, id_paymentmethod_id=1,
                       id_user_id=user_id, created=(timezone.now()))
    new_order.save()
    return new_order.id


def getActiveOrder(user_id):
    try:
        active_order = orders.objects.filter(id_user=user_id).latest('created')
        if active_order.finished:
            active_order = createNewOrder(user_id)
        else:
            active_order = active_order.id
        return active_order
    except orders.DoesNotExist:
        new_order_id = createNewOrder(user_id)
        return new_order_id

def getUsersOrders(request):
    """
    Get all orders with user id
    """
    id_user = request.GET.get('id', None)

    if not id_user:
        return HttpResponse(status=400)

    try:
        _orders = orders.objects.filter(id_user_id=id_user)
    except orders.DoesNotExist:
        _orders = None

    if _orders:
        _orders = _orders.values('id', 'firstname', 'lastname', 'email', 'phonenumber', 'adress', 'city', 'zipcode',
                                 'cardnumber', 'cardcsv', 'finished', 'created', 'id_deliverymethod',
                                 'id_paymentmethod', 'id_user', 'id_voucher')
        return JsonResponse(list(_orders), safe=False, status=200)

    return HttpResponse(status=404)


def getSpecificOrder(request):
    """
    Get specific user's order
    """

    id_order = request.GET.get('id', None)
    if not id_order:
        return HttpResponse(status=400)

    try:
        _order = orders.objects.get(id=id_order)
    except orders.DoesNotExist:
        _order = None

    if _order:
        return JsonResponse(model_to_dict(_order), safe=False, status=200)

    return HttpResponse(status=404)


@csrf_exempt
def createOrder(request):
    """
    Creating new order
    """

    data = json.loads(request.body)
    required = ['firstname', 'lastname', 'email', 'phonenumber', 'adress', 'city', 'zipcode', 'cardnumber',
                'cardcsv', 'finished', 'id_deliverymethod', 'id_paymentmethod', 'id_user', 'id_voucher']

    if not checkFilledFields(data, required):
        return HttpResponse(status=400)

    _order = orders(firstname=data['firstname'], lastname=data['lastname'], email=data['email'],
                    phonenumber=data['phonenumber'], adress=data['adress'], city=data['city'], zipcode=data['zipcode'],
                    cardnumber=data['cardnumber'], cardcsv=data['cardcsv'], finished=data['finished'],
                    id_deliverymethod_id=data['id_deliverymethod'], id_paymentmethod_id=data['id_paymentmethod'],
                    id_user_id=data['id_user'], id_voucher_id=data['id_voucher'], created=(timezone.now()))
    _order.save()
    return HttpResponse(status=200)


@csrf_exempt
def updateOrder(request):
    """
    Update an existing order
    """
    id_order = request.GET.get('id', None)
    data = json.loads(request.body)
    try:
        order = orders.objects.filter(id=id_order)
    except products.DoesNotExist:
        order = None

    if order:
        orders.objects.filter(id=id_order).update(**data)
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=404)


"""
------------- ORDER ITEMS REQUESTS -----------
"""


@csrf_exempt
def createCart(request):
    """
    Putting items to shopping cart
    """

    # data = json.loads(request.body)
    data = request.POST.dict()
    required = ['token', 'id_product_id']

    if not checkFilledFields(data, required):
        return HttpResponse(status=400)

    user_id = users.objects.get(token=data['token']).id
    id_order = getActiveOrder(user_id)


    basket = order_items(created=(timezone.now()), id_order_id=id_order, id_product_id=data['id_product_id'])
    basket.save()
    return HttpResponse(status=200)


@csrf_exempt
def removeFromCart(request):
    """
    Remove item from shopping cart
    """
    #id_order = request.GET.get('id_order', None)
    token = request.GET.get('token', None)
    id_product = request.GET.get('id_product', None)

    if not token or not id_product:
        return HttpResponse(status=400)

    user_id = users.objects.get(token=token).id
    id_order = getActiveOrder(user_id)

    try:
        data = order_items.objects.filter(id_order_id=id_order).filter(id_product_id=id_product)
    except order_items.DoesNotExist:
        data = None

    if not data:
        return HttpResponse(status=404)

    data.delete()
    return HttpResponse(status=200)

def getCartContent(request):
    """
    Show shopping cart content
    """

    token = request.GET.get('token', None)

    if not token:
        return HttpResponse(status=400)

    user_id = users.objects.get(token=token).id
    id_order = getActiveOrder(user_id)

    try:
        content = order_items.objects.filter(id_order_id=id_order)
    except order_items.DoesNotExist:
        content = None

    if content:
        content = list(content.values_list('id_product_id', flat=True))

        response = []
        for index in content:
            _product = products.objects.get(id=index)
            response.append({
                "id": _product.id,
                "title": _product.title,
                "description": _product.description,
                "image": str(_product.image.tobytes()),
                "price": _product.price
            })

        return JsonResponse(list(response), safe=False, status=200)

    return HttpResponse(status=404)
