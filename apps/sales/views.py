from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SaleForm
# Create your views here.


class CreateView(CreateView):
    template_name = 'sales/sale_form.html'
    form_class = SaleForm
    success_url = '/sales/sale/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)