
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/supplies/', include('supplies.urls')),
    path('api/movements/', include('movements.urls')),
    path('api/statistics/', include('stats.urls')),
]
