from django.shortcuts import render
from django.views.generic import CreateView,ListView
from .forms import SaleForm
from .models import Sale,SaleDetail,SalePlatform
from apps.products.models import Product
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# Create your views here.


class IndexView(ListView):
    template_name = 'in dex.html'
    model = Sale

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = Sale.objects.all()
        return context
    
@method_decorator(csrf_exempt, name='dispatch')
class CreateView(CreateView):
    template_name = 'base.html'
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
            product.stock -= amount
            if product.stock < 0:
                return JsonResponse({'message':f'Product {product} out of stock'}, status=400)
            sale_detail = SaleDetail.objects.create(product = product, unit_price = unit_price, amount = amount, sale = sale)
            sale_detail.total_price = unit_price * amount
            sale_detail.save()
            product.save()
            total += sale_detail.total_price
        sale.sub_total = total
        sale.total = total + (total * tax)
        sale.save()
        return JsonResponse({'message':'Sale created successfully'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class ListView(ListView):
    template_name = 'sales/sale_list.html'
    model = Sale

    def get(self, request, *args, **kwargs):
        return JsonResponse({'sales':list(Sale.objects.all().values())}, status=200)
