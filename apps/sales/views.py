from django.shortcuts import render,redirect
from django.views.generic import CreateView,DetailView,DeleteView,UpdateView
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
from django.contrib.messages.views import SuccessMessageMixin


class SaleIndexView(FilterView):
    template_name = 'sales/index.html'
    model = Sale
    paginate_by = 5
    filterset_class = SaleFilter
    context_object_name = 'sales'   

class SaleCreateView(SuccessMessageMixin,CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/form.html'
    success_url = reverse_lazy('sales:index')  
    success_message = "Elemento creado correctamente"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = kwargs.get('formset', DetalleVentaFormSet())
        data['products'] = Product.objects.all().order_by("name")
        return data

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleVentaFormSet(request.POST)
        form.formset = formset
        error_message = None
        if form.is_valid() and formset.is_valid():
            self.object = form.save() 
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        
        if not formset.is_valid():
            messages.error(request, "Es necesario agregar por lo menos un producto")
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'products': Product.objects.all()
        })

class SaleUpdateView(SuccessMessageMixin,UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/form.html'
    success_url = reverse_lazy('sales:index')
    success_message = "Elemento actualizado correctamente"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DetalleVentaFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = DetalleVentaFormSet(instance=self.object)

        data['products'] = Product.objects.all().order_by("name")
        return data
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = DetalleVentaFormSet(request.POST, instance=self.object)
        form.formset = formset
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'products': Product.objects.all()
        })

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sales/detail.html'
    context_object_name = 'sale'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = SaleDetail.objects.filter(sale=self.object)
        context['subtotal'] = sum([detail.total_price for detail in context['details']])
        context['iva'] = context['subtotal'] * Decimal(0.16)
        context['total'] = context['subtotal'] + context['iva']
        return context
    
class SaleDeleteView(SuccessMessageMixin,DeleteView):
    model = Sale
    success_url = reverse_lazy('sales:index')
    success_message = "Elemento eliminado correctamente"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(request, self.success_message)
        self.object.status = Sale.STATUS.CANCELLED
        self.object.save()
        return redirect(self.success_url)