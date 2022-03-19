from django.db import connections
from apiserver.models import *
from django.http import JsonResponse, HttpResponse
import json, random, string
from django.views.decorators.csrf import csrf_exempt

def tokenCreation():
    """
    Creation of unique token assigned to user
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k = 16))

def tokenIn(token):
    """
    ...
    """
    try:
        token_object = Users.objects.filter(token = token)
    except Users.DoesNotExist:
        token_object = None
    
    if token_object:
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
    rbody = request.body.decode('utf-8')
    rbody = json.loads(rbody)
    required = ['username', 'password']
    token = True

    if not checkFilledFields(rbody, required):
        return HttpResponse(status = 400)

    if request.method == 'GET':
        # tba
        return JsonResponse(data = None, status = 400, safe = False)
    elif request.method == 'POST':

        try:
            user = Users.objects.filter(username = rbody['username'])
        except Users.DoesNotExist:
            user = None
        
        if user:
            return HttpResponse(status = 409)
        else:
            while token:
                random_token = tokenCreation()
                token = tokenIn(random_token)

            _user = Users(username = rbody['username'], password = rbody['password'], token = random_token)
            _user.save()

        return HttpResponse(status = 201)

