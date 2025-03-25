from django import forms
from .models import Sale, SaleDetail
from django.forms import inlineformset_factory

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['client', 'address', 'platform', 'receipt_folio', 'status', 'date']
        widgets = {
            'client': forms.TextInput(attrs={
                'class': 'form-control', 
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border-style: solid; border-color: #529c43; width: 1365px; color: #529c43;',
                'placeholder': 'Juan Perez',
            }),
            # 'tax': forms.NumberInput(attrs={
            #     'class': 'form-control', 
            #     'value': 0.16, 
            #     'readonly': True,
            #     'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border-style: solid; border-color: #529c43;',
            # }),
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
DetalleVentaFormSet = inlineformset_factory(Sale, SaleDetail, form=SaleDetailForm, extra=1, can_delete=True)
