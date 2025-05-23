from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductIngredient

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category']

    formset = None

    def save(self, commit=True):
        product = super().save(commit=commit)

        formset = getattr(self, 'formset', None)
        if formset and commit:
            instances = formset.save(commit=False)

            # Guardar nuevos y modificados
            for instance in instances:
                instance.product = product
                instance.save()

            # Eliminar marcados como DELETE
            for obj in formset.deleted_objects:
                obj.delete()

        return product

class ProductIngredientForm(forms.ModelForm):
    class Meta:
        model = ProductIngredient
        fields = ['ingredient', 'amount']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

ProductIngredientFormSet = inlineformset_factory(
    Product,
    ProductIngredient,
    form=ProductIngredientForm,
    extra=0,
    can_delete=True,
)
