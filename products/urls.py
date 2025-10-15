from django.urls import path
from .views import * 

urlpatterns = [
    path('get', get_product, name='products_get'),
    path('get/<int:product_id>', get_product_by_id, name='product_by_id'),
    path('create',create_product, name='create_product'),
    path('total-stock', get_total_stock, name='total_stock'),
    path('total-stock-value', get_total_stock_value, name='total_stock_value'),
    path('get-categories', get_categories, name='categories'),
    path('update/<int:product_id>', update_product, name='update_product'),
    path('delete/<int:product_id>', delete_product, name='delete_product'),
]
