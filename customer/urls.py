from django.urls import path
from .views import registration,Sign_in,sign_out,index,user_home,item_detail,add_to_cart,view_mycart,base_home,remove_item


urlpatterns = [
    path('',index,name="index"),
    path('index',base_home,name="basepage"),
    path('account',registration,name="register"),

    path("login",Sign_in,name="login"),
    path("logout",sign_out,name="logout"),
    path("home",user_home,name="home"),
    path("item/<int:id>",item_detail,name="itemdetail"),
    path("carts/<int:id>",add_to_cart,name="add_to_cart"),
    path("carts",view_mycart,name="view_mycart"),
    path("remove/<int:id>",remove_item,name="remove")
    ]