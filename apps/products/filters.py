from apps.comun.filters import AbstractFilter
from .models import Product
import django_filters

productFields = {
    'name': {
        'label': 'Nombre'
    }
}
class ProductFilter(AbstractFilter):
    class Meta:
        model = Product
        fields = list(productFields.keys())
        fields_dict = productFields

