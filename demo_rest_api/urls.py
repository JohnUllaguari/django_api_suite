from django.urls import path
from . import views

urlpatterns = [
    # lista y creación de recursos
    path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_list"),

    # operaciones sobre un solo recurso (GET, PUT, PATCH, DELETE)
    path("<str:item_id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]
