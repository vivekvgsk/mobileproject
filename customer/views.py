from django.shortcuts import render,redirect
from customer.forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login as djangologin,logout
from django.contrib import messages
from owner.models import Product,Cart
from owner.views import get_object
from .decorators import loginrequired,permissionrequired
# Create your views here.

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
    context={
        "mobiles":mobiles
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
    context={
        "cart_items":cart_items
    }
    return render(request,"mycart.html",context)

@loginrequired
@permissionrequired
def remove_item(request,*args,**kwargs):
    pid=kwargs.get("id")
    item=Cart.objects.get(id=pid)
    item.delete()
    return redirect("view_mycart")