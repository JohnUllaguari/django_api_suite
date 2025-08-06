from django.urls import path
from . import views

urlpatterns = [
    # Listado y creación de recursos
    path('', views.DemoRestApi.as_view(), name='demo_rest_api_list'),
    # Operaciones sobre un solo recurso (GET, PUT, PATCH, DELETE)
    path('<str:item_id>/', views.DemoRestApiItem.as_view(), name='demo_rest_api_item'),
]

