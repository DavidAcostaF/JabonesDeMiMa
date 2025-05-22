from django import forms
from .models import Expense, ExpenseType

class ExpenseForm(forms.ModelForm):
    
    nueva_categoria = forms.CharField(
        required=False,
        label='Nueva categoría',
        widget=forms.TextInput(attrs={
            'class': 'form-control placeholder-green',
            'placeholder': 'Ej. Luz, Agua, Gasolina, etc.',
            'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
        })
    )

    type = forms.ChoiceField(
        label="Tipo de gasto",
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'padding: 12px; font-size: 27px; font-family: Lexend Deca, sans-serif; border-radius: 15px; border: 2px solid #529c43; color: #529c43',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generamos las opciones de tipo existentes + "otra"
        opciones = [(str(et.id), et.name) for et in ExpenseType.objects.all()]
        opciones.append(("otra", "Otra (crear nueva)"))
        self.fields['type'].choices = [("", "Selecciona una categoría")] + opciones

    def clean_type(self):
        value = self.cleaned_data.get("type")
        if value == "otra":
            return value
        try:
            return ExpenseType.objects.get(id=int(value))
        except (ExpenseType.DoesNotExist, ValueError, TypeError):
            raise forms.ValidationError("Categoría inválida.")

    class Meta:
        model = Expense
        fields = [
            'receipt_folio',
            'description',
            'date',
            'tax',
            'sub_total',
            'total',
            'proveedor',
        ]
        widgets = {
            'receipt_folio': forms.TextInput(attrs={
                'class': 'form-control placeholder-green',
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
                'placeholder': 'F000010',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control placeholder-green',
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
                'placeholder': 'Pago ejemplo',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': 'padding: 12px; font-size: 27px; font-family: Lexend Deca, sans-serif; border-radius: 15px; border: 2px solid #529c43; color: #529c43',
            }),
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'padding: 12px; font-size: 27px; font-family: Lexend Deca, sans-serif; border-radius: 15px; border: 2px solid #529c43; color: #529c43',
            }),
            'sub_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'padding: 12px; font-size: 27px; font-family: Lexend Deca, sans-serif; border-radius: 15px; border: 2px solid #529c43; color: #529c43',
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'style': 'padding: 12px; font-size: 27px; font-family: Lexend Deca, sans-serif; border-radius: 15px; border: 2px solid #529c43; color: #529c43',
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control placeholder-green',
                'style': 'font-family: "Lexend Deca", sans-serif; font-size: 27px; border-radius: 15px; padding: 10px; border: 2px solid #529c43; color: #529c43;',
                'placeholder': 'Proveedor Ejemplo',
        }),
        }
        labels = {
            'receipt_folio': 'Folio del comprobante',
            'description': 'Descripción',
            'type': 'Tipo de gasto',
            'date': 'Fecha',
            'tax': 'IVA',
            'sub_total': 'Subtotal',
            'total': 'Total',
            'proveedor': 'Proveedor',
        }
