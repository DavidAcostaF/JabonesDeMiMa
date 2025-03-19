from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SaleForm
from .models import Sale,SaleDetail,SalePlatform
from apps.products.models import Product
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class CreateView(CreateView):
    template_name = ''
    form_class = SaleForm
    success_url = reverse_lazy('sales:index')
    model = Sale
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode("utf-8"))
        client = json_data['client']
        address = json_data['address']
        platform = SalePlatform.objects.get(name=json_data['platform'])
        receipt_folio = json_data['receipt_folio']
        status = json_data['status']
        sale_details = json_data['sale_details']
        tax = 0.16
        sale = self.model.objects.create(client=client, tax=tax, address=address, platform=platform, receipt_folio=receipt_folio, status=status)
        total = 0
        for sale_detail in sale_details:
            product = Product.objects.get(name=sale_detail['product'])
            unit_price = sale_detail['unit_price']
            amount = sale_detail['amount']
            sale_detail = SaleDetail.objects.create(product = product, unit_price = unit_price, amount = amount, sale = sale)
            sale_detail.total_price = unit_price * amount
            sale_detail.save()
            product.stock -= amount
            product.save()
            total += sale_detail.total_price
        sale.sub_total = total
        sale.total = total + (total * tax)
        sale.save()
        return JsonResponse({'message':'Sale created successfully'}, status=200)



