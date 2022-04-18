from django.urls import path
from pip import main
from .views import main_view

urlpatterns = [
    path('', main_view, name='main_view')
]