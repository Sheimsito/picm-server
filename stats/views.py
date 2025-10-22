from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
import pytz
from django.core.cache import cache
from django.core.exceptions import ValidationError
import logging

from movements.models import ProductMovement, SupplyMovement
from products.models import Product, Category
from supplies.models import Supplies, Supplier
from .serializers import (
    TopProductsSalesSerializer,
    TopProductsEntriesSerializer,
    ProductMovementsVolumeSerializer,
    MonthlyMovementsResponseSerializer,
    TopSuppliesSalesSerializer,
    TopSuppliesEntriesSerializer,
    SupplyMovementsVolumeSerializer,
    CategoryDistributionResponseSerializer
)

logger = logging.getLogger(__name__)


class StatisticsBaseView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_date_filter(self, period):
        now = timezone.now()
        
        period_mapping = {
            '7d': now - timedelta(days=7),
            '30d': now - timedelta(days=30),
            '90d': now - timedelta(days=90),
            '1y': now - timedelta(days=365)
        }
        
        return period_mapping.get(period, period_mapping['30d'])
    
    def validate_period(self, period):
        valid_periods = ['7d', '30d', '90d', '1y']
        if period not in valid_periods:
            raise ValidationError(f"Período inválido. Debe ser uno de: {', '.join(valid_periods)}")
    
    def validate_limit(self, limit):
        try:
            limit = int(limit)
            if limit <= 0 or limit > 100:
                raise ValidationError("El límite debe estar entre 1 y 100")
            return limit
        except (ValueError, TypeError):
            raise ValidationError("El límite debe ser un número entero válido")


class TopProductsSalesView(StatisticsBaseView):
    
    def get(self, request):
        try:
            limit = self.validate_limit(request.GET.get('limit', 10))
            period = request.GET.get('period', '30d')
            self.validate_period(period)
            
            cache_key = f"top_products_sales_{period}_{limit}_{request.user.id}"
            
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            date_filter = self.get_date_filter(period)
            
            top_products = ProductMovement.objects.filter(
                modificationType='Salida',
                product__isnull=False,
                dateHourCreation__gte=date_filter,
                status=True
            ).select_related('product', 'product__category').values(
                'product__id',
                'product__name'
            ).annotate(
                total_sales=Count('id'),
                total_quantity=Sum('modifiedStock')
            ).order_by('-total_quantity')[:limit]
        
            data = []
            for item in top_products:
                product = Product.objects.get(id=item['product__id'])
                categories = product.category.all()
                category_name = ", ".join([cat.name for cat in categories]) if categories else "Sin categoría"
                
                data.append({
                    'product_id': item['product__id'],
                    'product_name': item['product__name'],
                    'total_sales': item['total_sales'],
                    'total_quantity': item['total_quantity'],
                    'category_name': category_name
                })
            
            response_data = {
                'data': data,
                'period': period,
                'total_products': len(data)
            }

            cache.set(cache_key, response_data, 30)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en TopProductsSalesView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopProductsEntriesView(StatisticsBaseView):
    
    def get(self, request):
        try:
            limit = self.validate_limit(request.GET.get('limit', 10))
            period = request.GET.get('period', '30d')
            self.validate_period(period)
            
            cache_key = f"top_products_entries_{period}_{limit}_{request.user.id}"
            
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            date_filter = self.get_date_filter(period)
            
            top_products = ProductMovement.objects.filter(
                modificationType='Entrada',
                product__isnull=False,
                dateHourCreation__gte=date_filter,
                status=True
            ).select_related('product', 'product__category').values(
                'product__id',
                'product__name'
            ).annotate(
                total_entries=Count('id'),
                total_quantity=Sum('modifiedStock')
            ).order_by('-total_quantity')[:limit]
            
            data = []
            for item in top_products:
                product = Product.objects.get(id=item['product__id'])
                categories = product.category.all()
                category_name = ", ".join([cat.name for cat in categories]) if categories else "Sin categoría"
                
                data.append({
                    'product_id': item['product__id'],
                    'product_name': item['product__name'],
                    'total_entries': item['total_entries'],
                    'total_quantity': item['total_quantity'],
                    'category_name': category_name
                })
            
            response_data = {
                'data': data,
                'period': period,
                'total_products': len(data)
            }
            
            cache.set(cache_key, response_data, 30)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en TopProductsEntriesView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductMovementsVolumeView(StatisticsBaseView):
    
    def get(self, request):
        try:
            period = request.GET.get('period', '30d')
            self.validate_period(period)
            
            cache_key = f"product_movements_volume_{period}_{request.user.id}"
            
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            date_filter = self.get_date_filter(period)
            
            movements_stats = ProductMovement.objects.filter(
                dateHourCreation__gte=date_filter,
                status=True
            ).aggregate(
                total_entries=Sum('modifiedStock', filter=Q(modificationType='Entrada')),
                total_sales=Sum('modifiedStock', filter=Q(modificationType='Salida')),
                total_movements=Count('id')
            )
            
            entries = movements_stats['total_entries'] or 0
            sales = movements_stats['total_sales'] or 0
            net_movement = entries - sales
            total_movements = movements_stats['total_movements'] or 0
            
            response_data = {
                'entries': entries,
                'sales': sales,
                'net_movement': net_movement,
                'period': period,
                'total_movements': total_movements
            }
            
            cache.set(cache_key, response_data, 30)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en ProductMovementsVolumeView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MonthlyMovementsView(StatisticsBaseView):
    
    def get(self, request):
        try:
            year = int(request.GET.get('year', timezone.now().year))
            movement_type = request.GET.get('type', 'both')  

            if year < 2020 or year > timezone.now().year + 1:
                raise ValidationError("Año inválido")
            
            if movement_type not in ['products', 'supplies', 'both']:
                raise ValidationError("Tipo debe ser 'products', 'supplies' o 'both'")
            
            cache_key = f"monthly_movements_{year}_{movement_type}_{request.user.id}"

            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            month_names = [
                'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
            ]
            
            data = []
            total_entries = 0
            total_sales = 0
            
            for month_num in range(1, 13):
                month_start = datetime(year, month_num, 1, tzinfo=pytz.UTC)
                if month_num == 12:
                    month_end = datetime(year + 1, 1, 1, tzinfo=pytz.UTC)
                else:
                    month_end = datetime(year, month_num + 1, 1, tzinfo=pytz.UTC)
                
                entries = 0
                sales = 0
                
                if movement_type in ['products', 'both']:
                    product_stats = ProductMovement.objects.filter(
                        dateHourCreation__gte=month_start,
                        dateHourCreation__lt=month_end,
                        status=True
                    ).aggregate(
                        entries=Sum('modifiedStock', filter=Q(modificationType='Entrada')),
                        sales=Sum('modifiedStock', filter=Q(modificationType='Salida'))
                    )
                    entries += product_stats['entries'] or 0
                    sales += product_stats['sales'] or 0
                '''
                # APPLY LATER
                 if movement_type in ['supplies', 'both']: 
                    supply_stats = SupplyMovement.objects.filter(
                        dateHourCreation__gte=month_start,
                        dateHourCreation__lt=month_end,
                        status=True
                    ).aggregate(
                        entries=Sum('modifiedStock', filter=Q(modificationType='Entrada')),
                        sales=Sum('modifiedStock', filter=Q(modificationType='Salida'))
                    )
                    entries += supply_stats['entries'] or 0
                    sales += supply_stats['sales'] or 0
                '''
                
                net_movement = entries - sales
                total_entries += entries
                total_sales += sales
                
                data.append({
                    'month': month_names[month_num - 1],
                    'month_number': month_num,
                    'entries': entries,
                    'sales': sales,
                    'net_movement': net_movement
                })
            
            response_data = {
                'data': data,
                'year': year,
                'total_entries': total_entries,
                'total_sales': total_sales
            }
            
            cache.set(cache_key, response_data, 100)
            return Response(response_data)
            
        except (ValueError, TypeError) as e:
            return Response({'error': 'Parámetros inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en MonthlyMovementsView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopSuppliesSalesView(StatisticsBaseView):
    
    def get(self, request):
        try:

            limit = self.validate_limit(request.GET.get('limit', 10))
            period = request.GET.get('period', '30d')
            self.validate_period(period)
            
            cache_key = f"top_supplies_sales_{period}_{limit}_{request.user.id}"
            
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            date_filter = self.get_date_filter(period)
            
            top_supplies = SupplyMovement.objects.filter(
                modificationType='EXIT',
                supply__isnull=False,
                dateHourCreation__gte=date_filter,
                status=True
            ).select_related('supply', 'supply__supplier').values(
                'supply__id',
                'supply__name',
                'supply__supplier__name'
            ).annotate(
                total_sales=Count('id'),
                total_quantity=Sum('modifiedStock')
            ).order_by('-total_quantity')[:limit]
            
            data = []
            for item in top_supplies:
                data.append({
                    'supply_id': item['supply__id'],
                    'supply_name': item['supply__name'],
                    'total_sales': item['total_sales'],
                    'total_quantity': item['total_quantity'],
                    'supplier_name': item['supply__supplier__name']
                })
            
            response_data = {
                'data': data,
                'period': period,
                'total_supplies': len(data)
            }
            
            cache.set(cache_key, response_data, 30)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en TopSuppliesSalesView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TopSuppliesEntriesView(StatisticsBaseView):
    
    def get(self, request):
        try:
            limit = self.validate_limit(request.GET.get('limit', 10))
            period = request.GET.get('period', '30d')
            self.validate_period(period)
            
           
            cache_key = f"top_supplies_entries_{period}_{limit}_{request.user.id}"
            
           
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            
            date_filter = self.get_date_filter(period)
            
           
            top_supplies = SupplyMovement.objects.filter(
                modificationType='ENTRY',
                supply__isnull=False,
                dateHourCreation__gte=date_filter,
                status=True
            ).select_related('supply', 'supply__supplier').values(
                'supply__id',
                'supply__name',
                'supply__supplier__name'
            ).annotate(
                total_entries=Count('id'),
                total_quantity=Sum('modifiedStock')
            ).order_by('-total_quantity')[:limit]
            
            data = []
            for item in top_supplies:
                data.append({
                    'supply_id': item['supply__id'],
                    'supply_name': item['supply__name'],
                    'total_entries': item['total_entries'],
                    'total_quantity': item['total_quantity'],
                    'supplier_name': item['supply__supplier__name']
                })
            
            response_data = {
                'data': data,
                'period': period,
                'total_supplies': len(data)
            }
            
            
            cache.set(cache_key, response_data, 30)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en TopSuppliesEntriesView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupplyMovementsVolumeView(StatisticsBaseView):
    
    
    def get(self, request):
        try:
            period = request.GET.get('period', '30d')
            self.validate_period(period)
            
            
            cache_key = f"supply_movements_volume_{period}_{request.user.id}"
            
            
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
           
            date_filter = self.get_date_filter(period)
            
          
            movements_stats = SupplyMovement.objects.filter(
                dateHourCreation__gte=date_filter,
                status=True
            ).aggregate(
                total_entries=Sum('modifiedStock', filter=Q(modificationType='ENTRY')),
                total_sales=Sum('modifiedStock', filter=Q(modificationType='EXIT')),
                total_movements=Count('id')
            )
            
            entries = movements_stats['total_entries'] or 0
            sales = movements_stats['total_sales'] or 0
            net_movement = entries - sales
            total_movements = movements_stats['total_movements'] or 0
            
            response_data = {
                'entries': entries,
                'sales': sales,
                'net_movement': net_movement,
                'period': period,
                'total_movements': total_movements
            }
            
          
            cache.set(cache_key, response_data, 30)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en SupplyMovementsVolumeView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDistributionView(StatisticsBaseView):
    
    
    def get(self, request):
        try:
            item_type = request.GET.get('type', 'products')  # 'products' o 'supplies'
            metric = request.GET.get('metric', 'stock')  # 'stock', 'value', 'movements'
            
            if item_type not in ['products', 'supplies']:
                raise ValidationError("Tipo debe ser 'products' o 'supplies'")
            
            if metric not in ['stock', 'value', 'movements']:
                raise ValidationError("Métrica debe ser 'stock', 'value' o 'movements'")
            
           
            cache_key = f"category_distribution_{item_type}_{metric}_{request.user.id}"
            
           
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
            
            data = []
            
            if item_type == 'products':
                
                categories = Category.objects.filter(status=True).prefetch_related('products')
                
                for category in categories:
                    products = category.products.filter(status=True)
                    
                    if metric == 'stock':
                        total_stock = sum(product.stock for product in products)
                        total_value = sum(float(product.price * product.stock) for product in products)
                    elif metric == 'value':
                        total_stock = sum(product.stock for product in products)
                        total_value = sum(float(product.price * product.stock) for product in products)
                    else:  
                        total_stock = sum(product.stock for product in products)
                        total_value = sum(float(product.price * product.stock) for product in products)
                    
                   
                    total_movements = 0
                    if metric == 'movements':
                        total_movements = ProductMovement.objects.filter(
                            product__in=products,
                            status=True
                        ).count()
                    
                    data.append({
                        'category_id': category.id,
                        'category_name': category.name,
                        'total_stock': total_stock,
                        'total_value': total_value,
                        'total_movements': total_movements,
                        'percentage': 0  
                    })
            
            else:  
                categories = Category.objects.filter(status=True)
                
                for category in categories:
                    
                    products = category.products.filter(status=True)
                    
                   
                    total_stock = 0
                    total_value = 0
                    total_movements = 0
                    
                    if metric == 'movements':
                        total_movements = SupplyMovement.objects.filter(
                            status=True
                        ).count()
                    
                    data.append({
                        'category_id': category.id,
                        'category_name': category.name,
                        'total_stock': total_stock,
                        'total_value': total_value,
                        'total_movements': total_movements,
                        'percentage': 0 
                    })
            

            if data:
                if metric == 'stock':
                    total_metric = sum(item['total_stock'] for item in data)
                elif metric == 'value':
                    total_metric = sum(item['total_value'] for item in data)
                else:  
                    total_metric = sum(item['total_movements'] for item in data)
                
                if total_metric > 0:
                    for item in data:
                        if metric == 'stock':
                            item['percentage'] = round((item['total_stock'] / total_metric) * 100, 2)
                        elif metric == 'value':
                            item['percentage'] = round((item['total_value'] / total_metric) * 100, 2)
                        else: 
                            item['percentage'] = round((item['total_movements'] / total_metric) * 100, 2)
            
            response_data = {
                'data': data,
                'total_categories': len(data),
                'metric': metric
            }
            
          
            cache.set(cache_key, response_data, 100)
            
            return Response(response_data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error en CategoryDistributionView: {str(e)}")
            return Response({'error': 'Error interno del servidor'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)