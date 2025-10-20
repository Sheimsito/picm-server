from django.urls import path
from .views import * 

urlpatterns = [
    # Product URLs
    path('get', get_product, name='products_get'),
    path('get/<int:product_id>', get_product_by_id, name='product_by_id'),
    path('create',create_product, name='create_product'),
    path('total-stock', get_total_stock, name='total_stock'),
    path('total-stock-value', get_total_stock_value, name='total_stock_value'),
    path('update/<int:product_id>', update_product, name='update_product'),
    path('update-stock/<int:product_id>', update_product_stock, name='update_product_stock'),
    path('delete/<int:product_id>', delete_product, name='delete_product'),

    # Category URLs
    path('get-categories', get_categories, name='categories'),
    path('get-categories-all', get_categories_all, name='categories_all'),
    path('get-category/<int:category_id>', get_category_by_id, name='category_by_id'),
    path('create-category', create_category, name='create_category'),
    path('update-category/<int:category_id>', update_category, name='update_category'),
    path('delete-category/<int:category_id>', delete_category, name='delete_category'),
    
]
