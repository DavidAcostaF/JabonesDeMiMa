from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import Product, ProductIngredient, Ingredient


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category']

    # Aquí inyectaremos el formset desde la vista
    formset = None

    def save(self, commit=True):
        product = super().save(commit=commit)

        # Si tiene un formset asociado, lo guarda
        formset = getattr(self, 'formset', None)
        if formset and commit:
            for ingredient_form in formset:
                if (ingredient_form.cleaned_data and 
                    not ingredient_form.cleaned_data.get('DELETE', False) and
                    ingredient_form.cleaned_data.get('ingredient') and
                    ingredient_form.cleaned_data.get('amount')):

                    ingredient = ingredient_form.save(commit=False)
                    ingredient.product = product
                    ingredient.save()

            return product


class ProductIngredientForm(forms.ModelForm):
    class Meta:
        model = ProductIngredient
        fields = ['ingredient', 'amount']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


# Formset con eliminación habilitada
ProductIngredientFormSet = inlineformset_factory(
    Product,
    ProductIngredient,
    form=ProductIngredientForm,
    extra=1,
    can_delete=True,
    validate_min=False  
)
