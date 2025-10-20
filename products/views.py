from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models.ProductM import Product
from .models.CategoryM import Category

class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

@api_view(['GET'])
def get_product(request):
    try:
        if 'search' in request.GET:
            search_term = request.GET['search']
            products = Product.objects.filter(name__icontains=search_term, status='1')
        else:
            products = Product.objects.filter(status='1')

        sort_by = request.query_params.get('filter')
        category_name = request.query_params.get('category')

        if category_name:
            products = products.filter(category__name__icontains=category_name)

        if sort_by  in ['price','-price', 'stock', '-stock']:
            products = products.order_by(sort_by)

        paginator = Pagination()
        result_page = paginator.paginate_queryset(products, request)
        data = [
            {
                "id": p.id, 
                "name": p.name,
                "description": p.description,
                "price": p.price, 
                "stock": p.stock,
                "category": p.returnCategoriesAsText()
            }
            for p in result_page
        ]
        return paginator.get_paginated_response(data)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_product_by_id(request, product_id):
    try:
        product = Product.objects.get(id=product_id, status='1')
        data = {
            "id": product.id, 
            "name": product.name,
            "description": product.description,
            "price": product.price, 
            "stock": product.stock,
            "category": product.returnCategoriesAsText()
        }
        return Response(data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_total_stock(request):
    try:
        total_products = Product.calculateTotalProducts()
        return Response({"total_products": total_products}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def get_total_stock_value(request):
    try:
        total_stock_value = Product.calculateTotalStock()
        return Response({"total_stock_value": total_stock_value}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_categories(request):
    try:
        categories = Category.objects.all()
        data = [{"name": c.name } for c in categories]
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def create_product(request):
    try:
        data = request.data
        name = data.get('nombre')
        description = data.get('descripcion')
        price = data.get('precio')
        category_name = data.get('categoria')

        category = Category.objects.filter(name=category_name).first()
        if category is None:
            return Response({"error": "La categoría especificada no existe."}, status=status.HTTP_409_CONFLICT)
        if not all([name, description, price, category]):
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_409_CONFLICT)
        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            status=True
        )
        product.category.set([category])
        return Response({"message": "Producto creado exitosamente", "product_id": product.id}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_product(request, product_id):
    try:
        data = request.data
        product = Product.objects.get(id=product_id, status='1')
        name = data.get('nombre')
        description = data.get('descripcion')
        price = data.get('precio')
        stock = data.get('stock')
        category_name = data.get('categoria')

        if category_name:
            category = Category.objects.filter(name=category_name).first()
            if category is None:
                return Response({"error": "La categoría especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)
            product.category.set([category])

        if name:
            product.name = name
        if description:
            product.description = description
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock

        product.save()
        return Response({"message": "Producto actualizado exitosamente"}, status=status.HTTP_200_OK)
    
    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id, status='1')
        product.status = False
        product.save()
        return Response({"message": "Producto eliminado exitosamente"}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_product_stock(request, product_id):
    try:
        print(request.data, request.query_params)
        product = Product.objects.get(id=product_id, status='1')
        data = request.data
        increase = request.query_params.get('increase') == 'true'
        decrease = request.query_params.get('decrease') == 'true'
        stock = data.get('stock')

        if increase and decrease:
            return Response({"error":"No puede usar increase y decrease al tiempo"}, status=400)

        if increase:
            if int(stock) < int(product.stock):
                return Response({"error": "El stock a aumentar debe ser mayor al actual"}, status=400)
            product.stock = stock if stock is not None else product.stock
            product.save()
            return Response({"message": "Stock aumentado", "stock": product.stock}, status=200)

        if decrease:
            if int(stock) < 0 or int(stock) > int(product.stock):
                return Response({"error": "El stock debe disminuir al valor actual y debe ser mayor que 0"}, status=400)
            product.stock = stock if stock is not None else product.stock
            product.save()
            return Response({"message": "Stock disminuido", "stock": product.stock}, status=200)

        # Si no viene increase/decrease, usar stock directo:
        stock = request.data.get('stock')
        if stock is None:
            return Response({"error": "Debe enviar increase/decrease o 'stock' en el body"}, status=400)
        if int(stock) < 0:
            return Response({"error": "Stock no puede ser negativo"}, status=400)

        product.stock = int(stock)
        product.save()
        return Response({"message": "Stock actualizado", "stock": product.stock}, status=200)

    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['GET'])
def get_categories_all(request):
    try:
        categories = Category.objects.filter(status=True)
        categories = categories.order_by('id')
        paginator = Pagination()
        result_page = paginator.paginate_queryset(categories, request)
        data = [{"id": c.id, "name": c.name, "description": c.description} for c in result_page]
        return paginator.get_paginated_response(data)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_category_by_id(request, category_id):
    try:
        if not category_id:
            return Response({"error": "El parámetro 'id' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.get(id=category_id, status=True)
        data = {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }
        return Response(data, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_category(request):
    try:
        data = request.data
        name = data.get('nombre')
        description = data.get('descripcion')

        if ( not name or name.strip() == "" ) or (not description or description.strip() == ""):
            return Response({"error": "Los campos son obligatorios."}, status=status.HTTP_409_CONFLICT)

        if Category.objects.filter(name=name).exists():
            return Response({"error": "La categoría ya existe."}, status=status.HTTP_409_CONFLICT)

        category = Category.objects.create(name=name, description=description)
        return Response({"message": "Categoría creada exitosamente", "category_id": category.id}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT'])
def update_category(request, category_id):
    try:
        data = request.data
        category = Category.objects.get(id=category_id)

        name = data.get('nombre')
        description = data.get('descripcion')

        if name:
            if Category.objects.filter(name=name).exclude(id=category_id).exists():
                return Response({"error": "Otra categoría con el mismo nombre ya existe."}, status=status.HTTP_409_CONFLICT)
            category.name = name
        if description:
            category.description = description

        category.save()
        return Response({"message": "Categoría actualizada exitosamente"}, status=status.HTTP_200_OK)
    
    except Category.DoesNotExist:
        return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
@api_view(['DELETE'])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.status = False
        category.save()
        return Response({"message": "Categoría eliminada exitosamente"}, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
