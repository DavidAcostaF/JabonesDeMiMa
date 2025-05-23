from django import forms
from .models import Expense, ExpenseType
from django.utils import timezone
from django.core.exceptions import ValidationError

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

    type = forms.CharField(
    label="Tipo de gasto",
    required=True,
    widget=forms.Select(attrs={
        'class': 'form-control',
        'style': 'padding: 12px; font-size: 27px; font-family: Lexend Deca, sans-serif; border-radius: 15px; border: 2px solid #529c43; color: #529c43',
    })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.errors.get(field):
                self.fields[field].widget.attrs.update({'class': self.fields[field].widget.attrs.get('class', '') + ' is-invalid'})

        # Generamos las opciones de tipo existentes + "otra"
        opciones = [(str(et.id), et.name) for et in ExpenseType.objects.all()]
        opciones.append(("otra", "Otra (crear nueva)"))
        # Construye manualmente el <select>
        self.fields['type'].widget.choices = [("", "Selecciona una categoría")] + opciones

        # Establecer valor inicial si es edición
        if self.instance and self.instance.pk and self.instance.type:
            self.fields['type'].initial = str(self.instance.type.id)

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('type')
        nueva = cleaned_data.get('nueva_categoria')
        subtotal = cleaned_data.get('sub_total')
        total = cleaned_data.get('total')

        if tipo == 'otra':
            if not nueva:
                self.add_error('nueva_categoria', 'Debes escribir un nombre para la nueva categoría.')
        elif not isinstance(tipo, ExpenseType):
            self.add_error('type', 'Debes seleccionar una categoría válida.')

        if subtotal is not None and subtotal <= 0:
            self.add_error('sub_total', 'El subtotal debe ser mayor a 0.')

        if total is not None and subtotal is not None and total < subtotal:
            self.add_error('total', 'El total no puede ser menor al subtotal.')

        return cleaned_data

    def clean_tax(self):
        tax = self.cleaned_data.get('tax')
        if tax is not None and tax < 0:
            raise ValidationError('El IVA no puede ser negativo.')
        return tax

    def clean_date(self):
        fecha = self.cleaned_data.get('date')
        if fecha and fecha.date() > timezone.now().date():
            raise ValidationError('La fecha no puede ser mayor a la actual.')
        return fecha

    def clean_nueva_categoria(self):
        nueva = self.cleaned_data.get('nueva_categoria')
        if nueva:
            if ExpenseType.objects.filter(name__iexact=nueva.strip()).exists():
                raise ValidationError('Ya existe una categoría con ese nombre.')
        return nueva

    def clean_type(self):
        value = self.cleaned_data.get("type")

        if not value:
            raise forms.ValidationError("Debes seleccionar una categoría o crear una nueva.")

        if value == "otra":
            # No devolver nada todavía, lo manejamos en clean()
            return value

        try:
            tipo = ExpenseType.objects.get(id=int(value))
            return tipo
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
