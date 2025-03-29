from django.urls import path
from .views import SaleCreateView,SaleDetailView,SaleIndexView,SaleDeleteView,SaleUpdateView

app_name = 'sales'

urlpatterns = [
    path('', SaleIndexView.as_view(), name='index'),
    path('create/', SaleCreateView.as_view(), name='create'),
    path('update/<int:pk>', SaleUpdateView.as_view(), name='update'),
    path('detail/<int:pk>', SaleDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', SaleDeleteView.as_view(), name='delete'),
]