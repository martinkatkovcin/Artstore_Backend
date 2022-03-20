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
    path('voucher', views.getVoucher, name = 'getVoucher'),
    path('products', views.getProducts, name = 'getProducts'),
    path('products/category', views.getProductsByCategory, name = 'getProductsByCategory'),
    path('product', views.getProduct, name = 'getProduct'),
    path('product/create', views.createProduct, name = 'createProduct'),
    path('product/update', views.updateProduct, name = 'updateProduct'),
    path('product/delete', views.deleteProduct, name = 'deleteProduct'),
    path('orders/<int:id_user>', views.getUsersOrders, name = 'getUserProducts'),
    path('order/<int:id_order>', views.getSpecificOrder, name = 'getSpecificOrder'),
    path('order/create', views.createOrder, name = 'createOrder')
]
