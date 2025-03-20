from django.urls import path
from .views import CreateView,ListView

app_name = 'sales'

urlpatterns = [
    path('create/', CreateView.as_view(), name='create'),
    path('list/', ListView.as_view(), name='list'),
]