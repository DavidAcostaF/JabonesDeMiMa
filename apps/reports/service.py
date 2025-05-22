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
        print("zxczxczxcData", data)
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
        timezone = 'America/Mexico_City'

        if self.filters['start_date'] and self.filters['end_date']:
            query &= Q(date__range=(self.filters['start_date'], self.filters['end_date']))
        elif self.filters['start_date']:
            query &= Q(date__date=self.filters['start_date'])
        elif self.filters['end_date']:
            query &= Q(date__date=self.filters['end_date'])

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