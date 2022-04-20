from django.contrib import admin
from django.urls import path, include
from apiserver import views

urlpatterns = [
    path('users/create', views.createUser, name = 'createUser'),
    path('users/update', views.updateUser, name = 'updateUser'),
    path('users/delete', views.deleteUser, name = 'deleteUser'),
    path('users/login', views.loginUser, name = 'loginuser'),
    path('users/info', views.getInfoUser, name = 'getInfoUser'),
    path('paymentmethods', views.getPaymentMethods, name = 'getPaymentMethods'),
    path('deliverymethods', views.getDeliveryMethods, name = 'getDeliveryMethods'),
    path('productcategories', views.getProductCategories, name = 'getProductCategories'),
    path('vouchers', views.getVouchers, name = 'getVouchers'),
    path('products', views.getProducts, name = 'getProducts'),
    path('product', views.getProduct, name = 'getProduct'),
    path('product/create', views.createProduct, name = 'createProduct'),
    path('product/update', views.updateProduct, name = 'updateProduct'),
    path('product/delete', views.deleteProduct, name = 'deleteProduct'),
    path('orders', views.getUsersOrders, name = 'getUsersOrders'),
    path('order', views.getSpecificOrder, name = 'getSpecificOrder'),
    path('order/create', views.createOrder, name = 'createOrder'),
    path('order/update', views.updateOrder, name = 'updateOrder'),
    path('cart/create', views.createCart, name = 'createCart'),
    path('cart/delete', views.removeFromCart, name='removeFromCart'),
    path('cart', views.getCartContent, name= 'getCartContent'),
    ]
