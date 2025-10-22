from django.urls import path
from .views import * 

urlpatterns = [
    path('get-movements', list_movements, name='list_product_movements'),
    path('get-movement/<int:movement_id>/<tipo_movimiento>', get_movement_by_id, name='get_movement_by_id'),
    path('update-movement/<int:movement_id>/<tipo_movimiento>', update_movement, name='update_movement'),
    path('create-movement/<tipo_movimiento>', create_movement, name='create_movement'),
    path('delete-movement/<int:movement_id>/<tipo_movimiento>', delete_movement, name='delete_movement'),
    ]