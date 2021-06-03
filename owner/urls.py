from django.urls import path
from .views import home,addbrand,listbrands,delete,updatebrand,product_create,list_products,edit_item,detail_product,remove_item

urlpatterns = [
    path('home',home,name="home"),
    path('brand',addbrand,name="add"),
    path('listbrands',listbrands,name="list"),
    path('delete<int:id>',delete,name="delete"),
    path('update<int:id>',updatebrand,name="update"),
    path('products',product_create,name="product"),
    path('items',list_products,name="items"),
    path('change/<int:id>',edit_item,name="change"),
    path('viewproduct/<int:id>',detail_product,name="viewproduct"),
    path('remove/<int:id>',remove_item,name="remove")
]
