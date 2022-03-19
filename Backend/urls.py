from django.contrib import admin
from django.urls import path
from apiserver import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uptime', views.uptime, name = 'uptime'),
    path('users/create', views.createUser, name = 'createUser'),
    path('users/update', views.updateUser, name = 'updateUser'),
    path('users/delete', views.deleteUser, name = 'deleteUser'),
    path('users/login', views.loginUser, name = 'loginuser'),
    path('users/info', views.getInfoUser, name = 'getInfoUser'),
    path('paymentmethods', views.getPaymentMethods, name = 'getPaymentMethods'),
    path('paymentmethod', views.getPaymentMethod, name = 'getPaymentMethod'),
    path('deliverymethods', views.getDeliveryMethods, name = 'getDeliveryMethods'),
    path('deliverymethod', views.getDeliveryMethod, name = 'getDeliveryMethod'),
    path('productcategories', views.getProductCategories, name = 'getProductCategories'),
    path('productcategory', views.getProductCategory, name = 'getProductCategory'),
]
