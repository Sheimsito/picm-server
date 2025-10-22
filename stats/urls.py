from django.urls import path
from . import views

urlpatterns = [
    # STATS PRODUCT ENDPOINTS
    path('top-products-sales/', views.TopProductsSalesView.as_view(), name='top-products-sales'),
    path('top-products-entries/', views.TopProductsEntriesView.as_view(), name='top-products-entries'),
    path('product-movements-volume/', views.ProductMovementsVolumeView.as_view(), name='product-movements-volume'),
    
    #STATS SUPPLY ENDPOINTS
    path('top-supplies-sales/', views.TopSuppliesSalesView.as_view(), name='top-supplies-sales'),
    path('top-supplies-entries/', views.TopSuppliesEntriesView.as_view(), name='top-supplies-entries'),
    path('supply-movements-volume/', views.SupplyMovementsVolumeView.as_view(), name='supply-movements-volume'),
    
    # GENERAL STATS ENDPOINTS
    path('monthly-movements/', views.MonthlyMovementsView.as_view(), name='monthly-movements'),
    path('category-distribution/', views.CategoryDistributionView.as_view(), name='category-distribution'),
]
