from django.urls import path
from . import views

urlpatterns = [
    path('product_movements_pdf', views.download_product_movements_pdf, name='download_product_movements_pdf'),
    path('download-product-report/<int:product_id>', views.download_product_movement_by_id, name='download_product_movement_by_id'),
    path('download-supply-report/<int:supply_id>', views.download_supply_movement_by_id, name='download_supply_movement_by_id'),
]