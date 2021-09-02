from django.urls import path

from .views import products, product, create_product

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('product/<int:pk>/', product, name='product'),
    path('create_product', create_product, name='create_product'),
]
