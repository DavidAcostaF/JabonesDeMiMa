from django.urls import path
from .views import CreateView,DetailView,IndexView

app_name = 'sales'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
]