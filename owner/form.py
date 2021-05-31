from django import forms
from .models import Brand

class BrandCreateForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields=["brand_name"]