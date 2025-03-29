from django import forms
from .models import Sale, SaleDetail
from django.forms import inlineformset_factory
from decimal import Decimal

class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.formset = kwargs.pop('formset', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.formset is not None and self.formset.is_valid():
            sub_total = 0
            details = self.formset.save(commit=False)

            for detail in details:
                detail.unit_price = detail.product.price
                detail.total_price = detail.unit_price * detail.amount
                detail.sale = instance
                sub_total += detail.total_price

            instance.sub_total = sub_total
            instance.total = sub_total + (sub_total * Decimal(0.16))

            if commit:
                instance.save()
                for detail in details:
                    detail.save()
                self.formset.save_m2m()
        elif self.formset is None:
            raise ValueError("SaleForm requires a formset to be passed.")

        return instance


    class Meta:
        model = Sale
        fields = ['client', 'address', 'platform', 'receipt_folio', 'status', 'date']
        widgets = {
            'client': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border-style: solid; border-color: #529c43; width: 1365px; color: #529c43;',
                'placeholder': 'Juan Perez',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border-style: solid; border-color: #529c43; width: 1365px; color: #529c43;',
                'placeholder': 'Av. Torres 1234',
            }),
            'platform': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'padding: 12px;font-size: 27px;font-family: Lexend Deca, sans-serif;border-radius: 15px;border: 2px solid #529c43;width: 645px;color: #529c43',
            }),
            'receipt_folio': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border-style: solid; border-color: #529c43; width: 520px; color: #529c43;',
                'placeholder': 'F000010',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'padding: 12px;font-size: 27px;font-family: Lexend Deca, sans-serif;border-radius: 15px;border: 2px solid #529c43;width: 645px;color: #529c43',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'padding: 12px;font-size: 27px;font-family: Lexend Deca, sans-serif;border-radius: 15px;border: 2px solid #529c43;width: 645px;color: #529c43',
            }),
        }
        labels = {
            'client': 'Cliente',
            'tax': 'Impuesto',
            'address': 'Dirección',
            'platform': 'Plataforma',
            'receipt_folio': 'Folio de recibo',
            'status': 'Estado',
            'date': 'Fecha',
        }


class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['product', 'amount']
        widgets = {
            'product': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }

# Inline formset factory
DetalleVentaFormSet = inlineformset_factory(Sale, SaleDetail, form=SaleDetailForm, extra=0, can_delete=True)
