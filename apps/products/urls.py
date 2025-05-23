from django.urls import path
from .views import ProductCreateView, ProductIndexView, ProductUpdateView, ProductDeleteView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductIndexView.as_view(), name='index'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('update/<int:pk>', ProductUpdateView.as_view(), name='update'),
    path('detail/<int:pk>', ProductDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
]
