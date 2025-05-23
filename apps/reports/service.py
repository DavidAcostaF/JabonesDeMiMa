import base64
import json
from datetime import datetime
from django.db.models import Count, Q
from apps.reports.utils import ReportGenerator  
from utils.annotate_functions import ToCharTZ
from django.db.models.functions import Coalesce
from django.db.models import Value
from apps.sales.models import Sale
from django.db.models import FloatField
from django.db.models.functions import Cast, Coalesce
from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils.timezone import make_aware

timezone = 'America/Mexico_City'

class SalesReportGenerator:
    """
    Class to generate sales reports in Excel format.
    """
    def __init__(self, filters):
        """
        Initialize the SalesReportGenerator with a request object.
        
        Parameters:
        request (HttpRequest): The request object containing user information.
        """
        self.filters = filters

    def generate_report(self):
        """
        Generate a sales report and return it as a base64 encoded string.
        """
        # Initialize the Excel workbook
        output, workbook = ReportGenerator.init_excel()
        ws_list = []
        data = self.get_sales()
        ws_list.append({
            "ws_name": "Sales",
            "columns": [
                "Fecha",
                "Folio",
                "Plataforma",
                "Dirección",
                "Cliente",
                "Estado",
                "Impuesto",
                "Subtotal",
                "Total"
                ],
            "data": data
        })
        ws_list_json = json.dumps(ws_list)
        ws_list_base64 = base64.b64encode(ws_list_json.encode('utf-8')).decode('utf-8')

        # Devolver los datos en formato JSON con codificación base64
        return {"data": ws_list_base64, "type": "json"}


    def get_sales(self):
        query = Q()

    # Obtener los strings
        start_date = self.filters.get('start_date')
        end_date = self.filters.get('end_date')

        start_date_parsed = parse_date_aware(start_date)
        end_date_parsed = parse_date_aware(end_date)
        # Construcción del filtro
        if start_date_parsed and end_date_parsed:
            query &= Q(date__range=(start_date_parsed, end_date_parsed))
        elif start_date_parsed:
            query &= Q(date__gte=start_date_parsed)
        elif end_date_parsed:
            query &= Q(date__lte=end_date_parsed)
        if self.filters.get('client'):
            query &= Q(client__icontains=self.filters.get('client'))
        if self.filters.get('platform'):
            query &= Q(platform=self.filters.get('platform'))

        data = Sale.objects.filter(query).annotate(
            fecha=ToCharTZ("date", timezone, "DD/MM/YYYY"),
            tax_f=Coalesce(Cast('tax', FloatField()), 0.0),
            subtotal_f=Coalesce(Cast('sub_total', FloatField()), 0.0),
            total_f=Coalesce(Cast('total', FloatField()), 0.0)
        ).values_list(
            'fecha',
            'receipt_folio',
            'platform__name',
            'address',
            'client',
            'status',
            'tax_f',
            'subtotal_f',
            'total_f'
        )
        print("Data", data)
        return list(data)
    
    # receipt_folio = models.CharField(max_length=100,unique=True,error_messages={'unique': 'Ya existe un registro con este folio.'})
    # date = models.DateTimeField()
    # status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.PENDING)
    # sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    # total = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    # platform = models.ForeignKey(SalePlatform, on_delete=models.CASCADE)
    # address = models.CharField(max_length=100)
    # tax = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    # client = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


def parse_date_aware(date_str):
    try:
        dt = datetime.strptime(date_str, "%d-%m-%Y")
        return make_aware(dt, timezone=ZoneInfo(timezone))
    except (ValueError, TypeError):
        return None