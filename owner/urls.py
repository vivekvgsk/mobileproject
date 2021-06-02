from django.urls import path
from .views import home,addbrand,listbrands,delete,updatebrand,product_create,list_products

urlpatterns = [
    path('home',home,name="home"),
    path('brand',addbrand,name="add"),
    path('listbrands',listbrands,name="list"),
    path('delete<int:id>',delete,name="delete"),
    path('update<int:id>',updatebrand,name="update"),
    path('products',product_create,name="product"),
    path('items',list_products,name="items")
]
