from django import forms
from .models import Sale,SaleDetail
from django.forms import inlineformset_factory

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['client', 'tax', 'address', 'platform',  'receipt_folio', 'status']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'value': 0.16, 'readonly': True}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'receipt_folio': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        # def save(self, commit=True):
        #     sale = super().save(commit=False)
        #     sale.sub_total = self.cleaned_data['sub_total']
        #     sale.total = self.cleaned_data['total']
        #     if commit:
        #         sale.save()
        #     return sale

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['product', 'amount']
        widgets = {
            'product': forms.HiddenInput(),  # Ensure the product field is treated as a hidden input
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


DetalleVentaFormSet = inlineformset_factory(Sale, SaleDetail, form=SaleDetailForm, extra=1, can_delete=True)