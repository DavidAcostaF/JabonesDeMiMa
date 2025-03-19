from django import forms
from .models import Sale,SaleDetail

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['client', 'tax', 'address', 'total', 'platform',  'receipt_folio', 'status', 'sub_total']
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'receipt_folio': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.ChoiceField(choices=Sale.STATUS.choices, widget=forms.Select(attrs={'class': 'form-control'})),
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
        fields = ['sale', 'product', 'unit_price', 'amount', 'total_price']
        widgets = {
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }