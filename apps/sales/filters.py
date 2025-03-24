from apps.comun.filters import AbstractFilter
from .models import Sale

sale_fields = {
    'date': {'label':"Fecha de venta"}
}
class SaleFilter(AbstractFilter):
    class Meta:
        model = Sale
        fields = list(sale_fields.keys())
        fields_dict = sale_fields