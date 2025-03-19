from django.test import TestCase
from django.urls import reverse
from .models import Sale

# Create your tests here.
class SaleFormViewTestCase(TestCase):

    def test_creacion_sale(self):
        datos = {
            'client': "Cliente Test",
            'tax': 10.50,
            'address': "Calle Falsa 123",
            'total': 110.50,
            'platform': 1,
            'user': 1,
            'receipt_folio': "FOLIO123",
            'status': "completed",
            'sub_total': 100.00
        }
        response = self.client.post(reverse('create'), data=datos)
        
        self.assertEqual(response.status_code, 302)  
        
        self.assertTrue(Sale.objects.filter(receipt_folio="FOLIO123").exists())