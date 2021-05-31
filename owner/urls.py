from django.urls import path
from .views import home,addbrand,listbrands,delete,updatebrand

urlpatterns = [
    path('home',home,name="home"),
    path('brand',addbrand,name="add"),
    path('listbrands',listbrands,name="list"),
    path('delete<int:id>',delete,name="delete"),
    path('update<int:id>',updatebrand,name="update")
]
