from django.urls import path
from .views import IndexView

app_name = 'dashboard'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]