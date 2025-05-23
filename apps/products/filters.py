from apps.comun.filters import AbstractFilter
from .models import Product
import django_filters

product_fields = {
    'name': ['icontains'],  # Permite búsqueda parcial por nombre
    'category': ['exact'],  # Filtrado exacto por categoría
    'price': ['gte', 'lte'],  # Precio mínimo y máximo
    'stock': ['gte', 'lte'],  # Stock mínimo y máximo
}

class ProductFilter(AbstractFilter):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nombre del producto',
        widget=django_filters.widgets.forms.TextInput(attrs={'class': 'form-control'})
    )
    category = django_filters.ModelChoiceFilter(
        field_name='category',
        queryset=Product.objects.none(),  # Se reemplazará en __init__
        label='Categoría',
        widget=django_filters.widgets.forms.Select(attrs={'class': 'form-control'})
    )
    price__gte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Precio mínimo',
        widget=django_filters.widgets.forms.NumberInput(attrs={'class': 'form-control'})
    )
    price__lte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Precio máximo',
        widget=django_filters.widgets.forms.NumberInput(attrs={'class': 'form-control'})
    )
    stock__gte = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='gte',
        label='Stock mínimo',
        widget=django_filters.widgets.forms.NumberInput(attrs={'class': 'form-control'})
    )
    stock__lte = django_filters.NumberFilter(
        field_name='stock',
        lookup_expr='lte',
        label='Stock máximo',
        widget=django_filters.widgets.forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = list(product_fields.keys())
        fields_dict = product_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar dinámicamente categorías si están disponibles
        self.filters['category'].queryset = self.queryset.model.category.field.remote_field.model.objects.all()
