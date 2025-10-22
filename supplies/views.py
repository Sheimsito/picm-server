from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models.SupplierM import Supplier
from .models.SuppliesM import Supplies
from movements.models import SupplyMovement

class StandardResultsSetPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = 'page_size'

@api_view(['GET'])

## Supply Views

def get_supplies(request):
    try:
        if 'search' in request.query_params:
            search_term = request.GET['search']
            supplies = Supplies.objects.filter(
                status=1,
                name__icontains=search_term
            )
        else:
            supplies = Supplies.objects.filter(status=1)
        
        supplier_name = request.query_params.get('supplier')
        sort_by = request.query_params.get('filter')

        if supplier_name:
            supplies = supplies.filter(supplier__name__icontains=supplier_name)
        if sort_by in ['unitaryPrice', '-unitaryPrice', 'stock', '-stock']:
            supplies = supplies.order_by(sort_by)
        
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(supplies, request)
        data = [
            {
                'id': supply.id,
                'name': supply.name,
                'description': supply.description,
                'unitaryPrice': supply.unitaryPrice,
                'stock': supply.stock,
                'supplier': supply.supplier.name,
            }
            for supply in result_page
        ]
        
        return paginator.get_paginated_response(data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_supply(request, supply_id):
    try:
        supply = Supplies.objects.get(id=supply_id, status=1)
        data = {
            'id': supply.id,
            'name': supply.name,
            'description': supply.description,
            'unitaryPrice': supply.unitaryPrice,
            'stock': supply.stock,
            'supplier': supply.supplier.name,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Supplies.DoesNotExist:
        return Response(
            {'error': 'Insumo no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_supplies_name(request):
    try:
        supply = Supplies.objects.filter(status=1)
        data = [s.name for s in supply]
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['POST'])
def create_supply(request):
    try:
        data = request.data
        name = data.get('nombre')
        description = data.get('descripcion')
        unitaryPrice = data.get('precio_unitario')
        supplier_name = data.get('proveedor')
        supplier = Supplier.objects.filter(name=supplier_name).first()
        new_supply = Supplies.objects.create(
            name=name,
            description=description,
            unitaryPrice=unitaryPrice,
            supplier=supplier
        )
        return Response({'message': 'El insumo creado exitosamente'},status=status.HTTP_201_CREATED
        )
    except Supplier.DoesNotExist:
        return Response(
            {'error': 'Supplier not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['PUT'])
def edit_supply(request, supply_id):
    try:
        data = request.data
        supply = Supplies.objects.get(id=supply_id)

        supply.name = data.get('nombre', supply.name)
        supply.description = data.get('descripcion', supply.description)
        supply.unitaryPrice = data.get('precio_unitario', supply.unitaryPrice)
        supply.stock = data.get('stock', supply.stock)

        supplier_name = data.get('proveedor')
        if supplier_name:
            supplier = Supplier.objects.get(name=supplier_name)
            supply.supplier = supplier

        supply.save()
        return Response({'message': 'Insumo actualizado exitosamente'}, status=status.HTTP_200_OK)
    except Supplies.DoesNotExist:
        return Response(
            {'error': 'Insumo no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Supplier.DoesNotExist:
        return Response(
            {'error': 'Proveedor no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR    
        )

@api_view(['PUT'])
def update_supply_stock(request, supply_id):
    try:
        supply = Supplies.objects.get(id=supply_id, status='1')
        data = request.data
        increase = request.query_params.get('increase') == 'true'
        decrease = request.query_params.get('decrease') == 'true'
        stock = data.get('stock')

        if increase and decrease:
            return Response({"error":"No puede usar increase y decrease al tiempo"}, status=400)

        if increase:
            if int(stock) < int(supply.stock):
                return Response({"error": "El stock a aumentar debe ser mayor al actual"}, status=400)
            supply.stock = stock if stock is not None else supply.stock
            supply.save()
            SupplyMovement.objects.create(
                user=request.user,
                user_name=request.user.username,
                supply=supply,
                supply_name=supply.name,
                modificationType='Incremento',
                modifiedStock=supply.stock
            )
            return Response({"message": "Stock aumentado", "stock": supply.stock}, status=200)

        if decrease:
            if int(stock) < 0 or int(stock) > int(supply.stock):
                return Response({"error": "El stock debe disminuir al valor actual y debe ser mayor que 0"}, status=400)
            supply.stock = stock if stock is not None else supply.stock
            supply.save()
            SupplyMovement.objects.create(
                user=request.user,
                user_name=request.user.username,
                supply=supply,
                supply_name=supply.name,
                modificationType='Disminución',
                modifiedStock=supply.stock
            )
            return Response({"message": "Stock disminuido", "stock": supply.stock}, status=200)

        # Si no viene increase/decrease, usar stock directo:
        stock = request.data.get('stock')
        if stock is None:
            return Response({"error": "Debe enviar increase/decrease o 'stock' en el body"}, status=400)
        if int(stock) < 0:
            return Response({"error": "Stock no puede ser negativo"}, status=400)

        supply.stock = int(stock)
        supply.save()
        return Response({"message": "Stock actualizado", "stock": supply.stock}, status=200)

    except Supplies.DoesNotExist:
        return Response({"error": "Insumo no encontrado"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_supply(request, supply_id):
    try:
        supply = Supplies.objects.get(id=supply_id)
        supply.status = False
        supply.save()
        return Response({'message': 'Insumo eliminado exitosamente'}, status=status.HTTP_200_OK)
    except Supplies.DoesNotExist:
        return Response(
            {'error': 'Insumo no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_supply_total_stock(request):
    try:
        total_stock = Supplies.calculate_total_supplies()
        return Response(
            {'total_stock': total_stock},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_supply_total_inventory_value(request):
    try:
        total_value = Supplies.calculate_total_inventory_value()
        return Response(
            {'total_inventory_value': total_value},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

## Supplier Views

@api_view(['GET'])
def get_suppliers(request):
    try:
        suppliers = Supplier.objects.all()
        data = [
            {
                'name': supplier.name
            }
            for supplier in suppliers
        ]
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET'])
def get_suppliers_paginated(request):
    try:
        if 'search' in request.query_params:
            search_term = request.GET['search']
            suppliers = Supplier.objects.filter(
                name__icontains=search_term
            )
        else:
            suppliers = Supplier.objects.all()
        
        paginator = StandardResultsSetPagination()
        result_page = paginator.paginate_queryset(suppliers, request)
        data = [
            {
                'id': supplier.id,
                'name': supplier.name,
                'nit': supplier.nit,
                'phone': supplier.phone,
                'email': supplier.email,
                'address': supplier.address
            }
            for supplier in result_page
        ]
        
        return paginator.get_paginated_response(data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['GET'])
def get_supplier_by_id(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        data = {
            'id': supplier.id,
            'name': supplier.name,
            'nit': supplier.nit,
            'phone': supplier.phone,
            'email': supplier.email,
            'address': supplier.address,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Supplier.DoesNotExist:
        return Response(
            {'error': 'Proveedor no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['POST'])
def create_supplier(request):
    try:
        data = request.data
        Supplier.objects.create(
                                name=data.get('name'),
                                nit= data.get('nit'),
                                phone= data.get('phone'),
                                email= data.get('email'),
                                address= data.get('address')
                                )
        return Response({'message': 'Proveedor creado exitosamente'},status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['PUT'])
def edit_supplier(request, supplier_id):
    try:
        data = request.data
        supplier = Supplier.objects.get(id=supplier_id)
        print(data)
        supplier.name = data.get('name', supplier.name)
        supplier.nit = data.get('nit', supplier.nit)
        supplier.phone = data.get('phone', supplier.phone)
        supplier.email = data.get('email', supplier.email)
        supplier.address = data.get('address', supplier.address)

        supplier.save()
        return Response({'message': 'Proveedor actualizado exitosamente'}, status=status.HTTP_200_OK)
    except Supplier.DoesNotExist:
        return Response(
            {'error': 'Proveedor no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR    
        )
    
@api_view(['DELETE'])
def delete_supplier(request, supplier_id):
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.delete()
        return Response({'message': 'Proveedor eliminado exitosamente'}, status=status.HTTP_200_OK)
    except Supplier.DoesNotExist:
        return Response(
            {'error': 'Proveedor no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )