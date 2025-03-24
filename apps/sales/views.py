from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView
from .forms import SaleForm
from .models import Sale,SaleDetail,SalePlatform
from apps.products.models import Product
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django_filters.views import FilterView
from .filters import SaleFilter
from .forms import SaleForm, DetalleVentaFormSet
from django.contrib import messages
from django.db.transaction import atomic

# Create your views here.
class IndexView(ListView):
    template_name = 'sales/index.html'
    model = Sale
    paginate_by = 20
    filterset_class = SaleFilter
    context_object_name = 'sales'   

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['sales'] = Sale.objects.all()
    #     return context

# @atomic
class CreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/create.html'
    success_url = reverse_lazy('sales:index')  # Redirige después de guardar

    def get_context_data(self, **kwargs):
        """Agrega el formset al contexto."""
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DetalleVentaFormSet(self.request.POST)
        else:
            data['formset'] = DetalleVentaFormSet()

        # Add the list of products
        data['products'] = Product.objects.all()
        return data

    def form_valid(self, form):
        """Ensure both the Sale and SaleDetails are saved correctly."""
        context = self.get_context_data()
        formset = context['formset']

        if form.is_valid() and formset.is_valid():
            self.object = form.save()  # Save the sale first
            formset.instance = self.object  # Assign sale to formset
            
            sale_details = formset.save(commit=False)
            sub_total = 0
            for detail in sale_details:
                detail.unit_price = detail.product.price
                detail.total_price = detail.unit_price * detail.amount
                detail.sale = self.object
                sub_total += detail.total_price
                detail.save()
            self.object.sub_total = sub_total
            print(self.object.tax)
            self.object.total = sub_total + (sub_total * self.object.tax)
            self.object.save()
            # Handle any m2m relationships (if needed)
            formset.save_m2m()

            messages.success(self.request, "Sale successfully created!")
            return redirect(self.get_success_url())
        else:
            # Debugging output
            print("Sale form errors:", form.errors)
            print("SaleDetail formset errors:", formset.errors)

            messages.error(self.request, "There was an error saving the sale.")
            return self.form_invalid(form)


# @method_decorator(csrf_exempt, name='dispatch')
# class CreateView(CreateView):
#     template_name = 'sales/create.html'
#     form_class = SaleForm
#     success_url = reverse_lazy('sales:index')
#     model = Sale
#     def post(self, request, *args, **kwargs):
#         json_data = json.loads(request.body.decode("utf-8"))
#         client = json_data['client']
#         address = json_data['address']
#         platform = SalePlatform.objects.get(name=json_data['platform'])
#         receipt_folio = json_data['receipt_folio']
#         status = json_data['status']
#         sale_details = json_data['sale_details']
#         tax = 0.16
#         sale = self.model.objects.create(client=client, tax=tax, address=address, platform=platform, receipt_folio=receipt_folio, status=status)
#         total = 0
#         for sale_detail in sale_details:
#             product = Product.objects.get(name=sale_detail['product'])
#             unit_price = sale_detail['unit_price']
#             amount = sale_detail['amount']
#             product.stock -= amount
#             if product.stock < 0:
#                 return JsonResponse({'message':f'Product {product} out of stock'}, status=400)
#             sale_detail = SaleDetail.objects.create(product = product, unit_price = unit_price, amount = amount, sale = sale)
#             sale_detail.total_price = unit_price * amount
#             sale_detail.save()
#             product.save()
#             total += sale_detail.total_price
#         sale.sub_total = total
#         sale.total = total + (total * tax)
#         sale.save()
#         return JsonResponse({'message':'Sale created successfully'}, status=200)

