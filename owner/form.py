from django import forms
from .models import Brand,Product


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields=["brand_name"]

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model=Product
        fields="__all__"
