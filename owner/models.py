from django.db import models

# Create your models here.
class Brand(models.Model):
    brand_name=models.CharField(max_length=120,unique=True)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    mobile_name=models.CharField(max_length=150,unique=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    price=models.IntegerField()
    specs=models.CharField(max_length=250)
    image=models.ImageField(upload_to="images")

    def __str__(self):
       return self.mobile_name
