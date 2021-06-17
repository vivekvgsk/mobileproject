from django.shortcuts import render,redirect
from customer.forms import UserRegistrationForm,LoginForm,PlaceOrderForm
from django.contrib.auth import authenticate,login as djangologin,logout
from django.contrib import messages
from owner.models import Product,Cart,Orders
from owner.views import get_object
from .decorators import loginrequired,permissionrequired
from django.db.models import Sum
# Create your views here.
def get_cart_count(user):
    cnt = Cart.objects.filter(user=user, status="Ordernotplaced").count()
    return cnt

def base_home(request):
    return render(request,"basehome.html")

def registration(request,*args,**kwargs):
    form=UserRegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            messages.error(request,"Sorry!!! Registration Failed")
            context["form"]=form
            return render(request,"registration.html",context)

    return render(request,"registration.html",context)

def Sign_in(request,*args,**kwargs):
    form=LoginForm()
    context={}
    context["form"]=form
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                djangologin(request,user)
                return redirect("home")
            else:
                messages.error(request,"invalid username or Paassword")
                return render(request, "login.html",context)
    return render(request,"login.html",context)


def sign_out(request,*args,**kwargs):
    logout(request)
    return redirect("login")

def index(request):
    return render(request,"home.html")

@loginrequired
def user_home(request,*args,**kwargs):

    mobiles=Product.objects.all()
    cnt=Cart.objects.filter(user=request.user,status="Ordernotplaced").count()
    print(cnt)
    context={
        "mobiles":mobiles,
        "cnt":cnt
    }
    return render(request,"userhome.html",context)

@loginrequired
def item_detail(request,*args,**kwargs):
    id=kwargs.get("id")
    mobile=Product.objects.get(id=id)
    context={
        "mobile":mobile
    }
    return render(request,"productdetail.html",context)

@loginrequired
def add_to_cart(request,*args,**kwargs):
    pid=kwargs.get("id")
    product=get_object(pid)
    cart=Cart(product=product,user=request.user) #ORM query for adding an element to a model(here Cart)
    cart.save()
    return redirect("view_mycart")

@loginrequired

def view_mycart(request,*args,**kwargs):
    cart_items=Cart.objects.filter(user=request.user,status="Ordernotplaced")
    total = Cart.objects.filter(status='Ordernotplaced', user=request.user).aggregate(Sum('product__price'))
    cnt = Cart.objects.filter(user=request.user, status="Ordernotplaced").count()

    context={
        "cart_items":cart_items,
        "total":total.get("product__price__sum"),
        "cnt":cnt
    }
    return render(request,"mycart.html",context)

@loginrequired
@permissionrequired
def remove_item(request,*args,**kwargs):
    pid=kwargs.get("id")
    item=Cart.objects.get(id=pid)
    item.delete()
    return redirect("view_mycart")


def place_order(request,*args,**kwargs):
    pid=kwargs.get("id")
    mobile=get_object(pid)
    # customer=Orders.objects.filter(user=request.user)
    cnt=get_cart_count(request.user)
    context={
        "form":PlaceOrderForm(initial={"product":mobile.mobile_name}),
           "cnt":cnt
    }
    print(kwargs)
    if request.method=="POST":
        cid=kwargs.get("cid")
        cart=Cart.objects.get(id=cid)
        print(kwargs)
        form=PlaceOrderForm(request.POST)
        if form.is_valid():
            address=form.cleaned_data.get("address")
            product=mobile
            order=Orders(address=address,product=product,user=request.user)
            order.save()
            cart.status="oredrplaced"
            cart.save()
            return redirect("myorders")

    return render(request,"placeorder.html",context)

def view_my_orders(request,*args,**kwargs):
    order_items=Orders.objects.filter(user=request.user)
    context={}
    context["order_items"]=order_items
    cnt=get_cart_count(request.user)
    context["cnt"]=cnt
    return render(request,"myorders.html",context)

@loginrequired

def cancel_order(request,*args,**kwargs):
    pid=kwargs.get("id")
    item=Orders.objects.get(id=pid)
    item.status="cancelled"
    item.save()
    return redirect("myorders")

