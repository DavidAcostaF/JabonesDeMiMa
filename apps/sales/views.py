from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView,DetailView
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
from decimal import Decimal

# Create your views here.
class IndexView(FilterView):
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
        # print(self.object)
        print("formset",formset)

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
            self.object.total = sub_total + (sub_total * Decimal(0.16))
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

    def form_invalid(self, form):
        """Handle invalid form submissions."""
        messages.error(self.request, "There was an error saving the sale.")
        print(form)
        return super().form_invalid(form)
    

class DetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
    context_object_name = 'sale'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = SaleDetail.objects.filter(sale=self.object)
        return context