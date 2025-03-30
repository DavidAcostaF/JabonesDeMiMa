from apps.comun.filters import AbstractFilter
from .models import Sale
import django_filters

sale_fields = {
    
}
class SaleFilter(AbstractFilter):
    fecha = django_filters.DateFromToRangeFilter(
        field_name='date',
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Seleccione el rango de fechas y horas'
            }
        ),
        label='Rango de fechas',
    )
    class Meta:
        model = Sale
        fields = list(sale_fields.keys())
        fields_dict = sale_fields