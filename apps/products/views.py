from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django_filters.views import FilterView
from apps.products.filters import ProductFilter
from .models import Ingredient, Product, ProductIngredient
from .forms import ProductForm, ProductIngredientForm, ProductIngredientFormSet
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.forms import inlineformset_factory
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('products:index')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = ProductIngredientFormSet(prefix='ingredients')
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'ingredients': Ingredient.objects.all().order_by('name'),
            "action_type": "Crear"
        })
    
    def post(self, request, *args, **kwargs): 
        form = self.form_class(request.POST)
        formset = ProductIngredientFormSet(request.POST, prefix='ingredients')

        if form.is_valid() and formset.is_valid():
            form.formset = formset
            product = form.save()
            for ingredient_form in formset:
                # Saltar formularios vacíos o marcados para eliminar
                if (ingredient_form.cleaned_data and 
                    not ingredient_form.cleaned_data.get('DELETE') and 
                    ingredient_form.cleaned_data.get('ingredient') and 
                    ingredient_form.cleaned_data.get('amount')):

                    ingredient = ingredient_form.save(commit=False)
                    ingredient.product = product
                    ingredient.save()
                    messages.success(request, "Producto creado correctamente")  
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'ingredients': Ingredient.objects.all().order_by('name')
        })

    
class ProductIndexView(FilterView):
    model = Product
    template_name = 'products/index.html'  # Asegúrate de crear este template
    context_object_name = 'products'
    paginate_by = 7
    filterset_class = ProductFilter

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/form.html"
    success_url = reverse_lazy("products:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = ProductIngredientFormSet(self.request.POST, instance=self.object)
        else:
            context["formset"] = ProductIngredientFormSet(instance=self.object)

        context["ingredients"] = Ingredient.objects.all()
        context["action_type"] = "Actualizar"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if formset.is_valid():
            form.formset = formset
            self.object = form.save()
            messages.success(self.request, "Producto actualizado correctamente")
            return redirect(self.success_url)
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