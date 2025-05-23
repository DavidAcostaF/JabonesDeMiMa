from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .models import Product
from .forms import ProductForm, ProductIngredientFormSet
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.forms import inlineformset_factory
from django.views.generic import DeleteView
from django.views.generic import DetailView

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'  # Asegúrate de que este sea el template correcto
    success_url = reverse_lazy('products:index')  # Cambia según tu ruta de éxito

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = ProductIngredientFormSet()
        return render(request, self.template_name, {
            'form': form,
            'formset': formset
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = ProductIngredientFormSet(request.POST)

        form.formset = formset  # Importante: pasa el formset al form como en SaleForm

        if form.is_valid() and formset.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset
        })
    
class ProductIndexView(ListView):
    model = Product
    template_name = 'products/index.html'  # Asegúrate de crear este template
    context_object_name = 'products'

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ProductIngredientFormSet = inlineformset_factory(
            Product, ProductIngredient, form=ProductIngredientForm,
            extra=1, can_delete=True
        )
        if self.request.POST:
            data['formset'] = ProductIngredientFormSet(self.request.POST, instance=self.object)
        else:
            data['formset'] = ProductIngredientFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = reverse_lazy('products:index')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = ProductIngredient.objects.filter(product=self.object)
        return context