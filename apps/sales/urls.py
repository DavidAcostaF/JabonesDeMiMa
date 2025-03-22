from django.urls import path
from .views import CreateView,ListView,IndexView

app_name = 'sales'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('list/', ListView.as_view(), name='list'),
]