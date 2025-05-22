from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.index, name='index'),           
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('grupo/<str:tipo>/', views.detail_group, name='detail_group'),
]