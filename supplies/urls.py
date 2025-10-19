from django.urls import path
from .views import * 

urlpatterns = [
    #  Supplies URLs
    path('get-paginated', get_supplies, name='get_supplies'),
    path('create', create_supply, name='create_supply'),
    path('total-stock', get_supply_total_stock, name='get_supply_total_stock'),
    path('total-inventory-value', get_supply_total_inventory_value, name='get_supply_total_inventory_value'),
    path('delete/<int:supply_id>', delete_supply, name='delete_supply'),
    path('update/<int:supply_id>', edit_supply, name='update_supply'),
    path('get/<int:supply_id>', get_supply, name='get_supply'),

    # Supplier URLs
    
    path('get-suppliers', get_suppliers, name='get_suppliers'),
    path('get-suppliers-paginated', get_suppliers_paginated, name='get_suppliers_paginated'),
    path('create-supplier', create_supplier, name='create_supplier'),
    path('delete-supplier/<int:supplier_id>', delete_supplier, name='delete_supplier'),
    path('update-supplier/<int:supplier_id>', edit_supplier, name='edit_supplier'),
    path('get-supplier/<int:supplier_id>', get_supplier_by_id, name='get_supplier'),
]