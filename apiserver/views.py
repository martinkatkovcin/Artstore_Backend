from collections import UserString
from multiprocessing.sharedctypes import Value
from django.db import connections
from apiserver.models import *
from django.http import JsonResponse, HttpResponse
import json, random, string, re
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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
        _user = {"firstName" : user.firstName,
                "lastName" : user.lastName,
                "username" : user.username,
                "password" : user.password,
                "email" : user.email,
                "phoneNumber" : user.phoneNumber,
                "token" : user.token}
        
        response.update(_user)
        print(response)
        return JsonResponse(response, status = 200, safe = False)
    
    else:
        return HttpResponse(status = 404)
