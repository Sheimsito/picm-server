from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from products.views import update_product_stock ## ADD LATER 
from supplies.views import update_supply_stock ## ADD LATER
from .models import ProductMovement
from .models import SupplyMovement
from products.models import Product
from supplies.models import Supplies
from django.contrib.auth.models import User
from django.utils import timezone

class MovementsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

@api_view(['GET'])
def list_movements(request):
    tipo = request.GET.get("tipo_movimiento")

    if tipo == "productos":
        Model = ProductMovement
        filter_key = "product__name__icontains"
        name_field = "product"
    else:
        Model = SupplyMovement
        filter_key = "supply__name__icontains"
        name_field = "supply"

    filters = {}
    q = request.GET.get('search')
    if q: filters[filter_key] = q
    if t := request.GET.get('movement_type'): filters['modificationType'] = t
    if fd := request.GET.get('fecha_desde'):   filters['dateHourCreation__gte'] = fd
    if fh := request.GET.get('fecha_hasta'):   filters['dateHourCreation__lte'] = fh

    qs = Model.objects.filter(**filters, status=True)

    paginator = MovementsPagination()
    page = paginator.paginate_queryset(qs, request)               

    data = []
    for m in page:
        data.append({
            "id": m.id,
            name_field: getattr(m, name_field).name,
            "user": m.user.username,
            "modificationType": m.modificationType,
            "modifiedStock": m.modifiedStock,
            "comentary": m.comentary,
            "dateHourCreation": m.dateHourCreation,
            "dateHourUpdate": m.dateHourUpdate,
        })
    print(data)
    return paginator.get_paginated_response(data)

@api_view(['GET'])
def get_movement_by_id(request, movement_id,tipo_movimiento):
    tipo = tipo_movimiento

    if tipo == "productos":
        Model = ProductMovement
    elif tipo == "insumos":
        Model = SupplyMovement
    else:
        return Response({"error": "tipo_movimiento inválido"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        movement = Model.objects.get(id=movement_id)
    except Model.DoesNotExist:
        return Response({"error": "Movimiento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "user": movement.user.username,
        "modificationType": movement.modificationType,
        "modifiedStock": movement.modifiedStock,
        "comentary": movement.comentary,
        "dateHourCreation": movement.dateHourCreation
    }

    if tipo == "productos":
        data["product"] = movement.product.name
    else:
        data["supply"] = movement.supply.name

    print(data)

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_movement(request, tipo_movimiento):
    if tipo_movimiento not in ("productos", "insumos"):
        return Response({"error": "tipo_movimiento inválido"}, status=400)

    Model = ProductMovement if tipo_movimiento == "productos" else SupplyMovement
    data = request.data

    try:     
        user = User.objects.get(username=data.get("user"))
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)


    modification_type = data.get("modificationType")
    modified_stock   = data.get("modifiedStock")

    if not modification_type or not modified_stock:
        return Response({"error": "Faltan campos obligatorios"}, status=400)

    if tipo_movimiento == "productos":
        product = Product.objects.filter(name=data.get("product_name")).first()
        if not product:
            return Response({"error": "Producto no encontrado"}, status=404)
        target_fk_field = {"product": product, "product_name": product.name}

    else:  
        supply = Supplies.objects.filter(name=data.get("supply_name")).first()
        if not supply:
            return Response({"error": "Insumo no encontrado"}, status=404)
        target_fk_field = {"supply": supply, "supply_name": supply.name}


    Model.objects.create(
        user=user,
        user_name=user.username,
        modificationType=modification_type,
        modifiedStock=modified_stock,
        comentary=data.get("comentary", ""),
        **target_fk_field
    )

    return Response(
        {"message": "El movimiento se creó exitosamente."},
        status=201
    )

@api_view(['PUT'])
def update_movement(request, movement_id, tipo_movimiento):
    tipo = tipo_movimiento

    if tipo not in ("productos", "insumos"):
        return Response({"error": "tipo_movimiento inválido"}, status=status.HTTP_400_BAD_REQUEST)

    Model = ProductMovement if tipo == "productos" else SupplyMovement

    try:
        movement = Model.objects.get(id=movement_id)
    except Model.DoesNotExist:
        return Response({"error": "Movimiento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    user_name = data.get("user")
    if user_name:
        try:
            user = User.objects.get(username=user_name)
            movement.user = user
            movement.user_name = user.username
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Campos comunes
    for field in ( "modificationType", "modifiedStock", "comentary"):
        if field in data:
            setattr(movement, field, data[field])

    # Campos específicos según tipo
    if tipo == "productos" and "product_name" in data:
        product = Product.objects.filter(name=data["product_name"]).first()
        if not product:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            movement.product = product

    if tipo == "insumos" and "supply_name" in data:
        supply = Supplies.objects.filter(name=data["supply_name"]).first()
        if not supply:
            return Response({"error": "Insumo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            movement.supply = supply


    if date_hour_creation := data.get("dateHourCreation"):
        movement.dateHourCreation = date_hour_creation
    movement.save()

    return Response(
        {"message": "El movimiento se editó exitosamente."},
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete_movement(request, movement_id, tipo_movimiento):
    tipo = tipo_movimiento

    if tipo not in ("productos", "insumos"):
        return Response({"error": "tipo_movimiento inválido"}, status=status.HTTP_400_BAD_REQUEST)

    Model = ProductMovement if tipo == "productos" else SupplyMovement

    try:
        movement = Model.objects.get(id=movement_id)
    except Model.DoesNotExist:
        return Response({"error": "Movimiento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    movement.status = False
    movement.dateHourDeletion = timezone.now()

    movement.save()

    return Response(
        {"message": "El movimiento se eliminó exitosamente."},
        status=status.HTTP_200_OK
    )
