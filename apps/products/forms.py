from django import forms
from .models import Product, ProductIngredient
from django.forms import inlineformset_factory
from decimal import Decimal
import re

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.formset = kwargs.pop('formset', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.formset is not None and self.formset.is_valid():
            if commit:
                instance.save()
                details = self.formset.save(commit=False)

                for detail in details:
                    detail.product = instance
                    detail.save()

                for obj in self.formset.deleted_objects:
                    obj.delete()

                self.formset.save_m2m()
        elif self.formset is None:
            raise ValueError("ProductForm requires a formset to be passed.")

        return instance

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", name):
            raise forms.ValidationError("No se permiten caracteres especiales en el nombre.")
        return name

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto',
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio',
                'style': 'font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Stock',
                'style': 'font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
            }),
        }
        labels = {
            'name': 'Nombre del producto',
            'price': 'Precio',
            'stock': 'Stock disponible',
            'category': 'Categoría',
        }

class ProductIngredientForm(forms.ModelForm):
    class Meta:
        model = ProductIngredient
        fields = ['ingredient', 'amount']
        widgets = {
            'ingredient': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-size: 20px; border-radius: 10px; padding: 8px;',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'font-size: 20px; border-radius: 10px; padding: 8px;',
                'min': '0.01',
                'step': '0.01'
            }),
        }
        labels = {
            'ingredient': 'Ingrediente',
            'amount': 'Cantidad',
        }

# Inline formset factory
ProductIngredientFormSet = inlineformset_factory(
    Product,
    ProductIngredient,
    form=ProductIngredientForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)



           
                

            

   