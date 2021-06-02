from django.shortcuts import render,redirect
from .models import Brand,Product
from .form import BrandCreateForm,ProductCreateForm

# Create your views here.
def home(request):
    return render(request,"index.html")

def addbrand(request):
    if request.method=="GET":
        form=BrandCreateForm()
        context={}
        context["form"]=form
        return render(request,"createbrand.html",context)
    elif request.method=="POST":
        form=BrandCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list")
def listbrands(request):
    brands=Brand.objects.all()
    context={}
    context["brands"]=brands
    return render(request,"listbrands.html",context)

def delete(request,id):
    brand=Brand.objects.get(id=id)
    brand.delete()
    return redirect("list")

def updatebrand(request,id):
    brand=Brand.objects.get(id=id)
    instance={
        "brand_name":brand.brand_name
    }
    form=BrandCreateForm(instance=brand)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=BrandCreateForm(instance=brand ,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("list")
    return render(request,"updatebrand.html",context)

def product_create(request):
    form=ProductCreateForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ProductCreateForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'mobilelist.html',context)

    return render(request,'productcreate.html',context)
def list_products(request):
    mobiles=Product.objects.all()
    context={}
    context["mobiles"]=mobiles
    return render(request,"mobilelist.html",context)