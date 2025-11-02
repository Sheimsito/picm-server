from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.http import require_GET
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from movements.models import ProductMovement
from movements.models import SupplyMovement
from .pdfGenerator import generate_movements_pdf
import datetime

@api_view(['GET'])
def download_product_movements_pdf(request):
    qs = ProductMovement.objects.filter(status=1).order_by('dateHourCreation')[:1000]
    columns = ['ID', 'Producto', 'Cantidad', 'Tipo', 'Usuario', 'Fecha', 'Comentario']
    rows = []
    for m in qs:
        rows.append([
            m.id,
            getattr(m, 'product_name', '') or (m.product.name if getattr(m, 'product', None) else ''),
            getattr(m, 'modifiedStock', m.modified_stock if hasattr(m, 'modified_stock') else ''),
            getattr(m, 'modificationType', m.modificationType if hasattr(m, 'modificationType') else ''),
            getattr(m, 'user_name', '') or (m.user.username if getattr(m, 'user', None) else ''),
            (m.dateHourCreation.strftime('%Y/%m/%d') if getattr(m, 'dateHourCreation', None) else ''),
            getattr(m, 'comentary', '') or getattr(m, 'description', '') or ''
        ])
    meta_title = "Movimientos de Productos"
    fecha_hora = datetime.datetime.now().isoformat()
    buf = generate_movements_pdf(rows, columns, doc_title=meta_title, fecha_hora=fecha_hora, logo_path=None)
    return FileResponse(buf, as_attachment=True, filename='movimientos_productos.pdf')

@require_GET
def download_product_movement_by_id(request, product_id):
    try:
        movement = ProductMovement.objects.get(id=product_id)
        
        columns = ['ID','Producto','Usuario','Tipo','Stock','Comentario','Fecha Creación','Fecha Modificación']
        rows = [[
            movement.id,
            movement.product_name,
            movement.user_name,
            movement.modificationType,
            movement.modifiedStock,
            movement.comentary,
            movement.dateHourCreation.strftime('%Y/%m/%d') if movement.dateHourCreation else '',
            movement.dateHourUpdate.strftime('%Y/%m/%d') if movement.dateHourUpdate else ''
        ]]

        title = "Movimiento de Producto"
        fecha_hora = datetime.datetime.now().isoformat()

        buf = generate_movements_pdf(rows, columns, title, fecha_hora, None)
        return FileResponse(buf, as_attachment=True, filename=f'movimiento_{movement.id}.pdf')

    except ProductMovement.DoesNotExist:
        return Response({'error': 'Movimiento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@require_GET
def download_supply_movement_by_id(request, supply_id):
    try:
        movement = SupplyMovement.objects.get(id=supply_id)

        columns = ['ID','Insumo','Usuario','Tipo','Stock','Comentario','Fecha Creación','Fecha Modificación']
        rows = [[
            movement.id,
            movement.supply_name,
            movement.user_name,
            movement.modificationType,
            movement.modifiedStock,
            movement.comentary,
            movement.dateHourCreation.strftime('%Y/%m/%d') if movement.dateHourCreation else '',
            movement.dateHourUpdate.strftime('%Y/%m/%d') if movement.dateHourUpdate else ''
        ]]

        title = "Movimiento de Insumo"
        fecha_hora = datetime.datetime.now().isoformat()

        buf = generate_movements_pdf(rows, columns, title, fecha_hora, None)
        return FileResponse(buf, as_attachment=True, filename=f'movimiento_{movement.id}.pdf')

    except SupplyMovement.DoesNotExist:
        return Response({'error': 'Movimiento no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)