from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models.ProductM import Product
from .models.CategoryM import Category

class ProductPagination(PageNumberPagination):
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
            products = products.filter(category__name=category_name)

        if sort_by == 'low-price':
            products = products.order_by('price')
        elif sort_by == 'high-price':
            products = products.order_by('-price')
        elif sort_by == 'low-stock':
            products = products.order_by('stock')
        elif sort_by == 'high-stock':
            products = products.order_by('-stock')
        else:
            products = products.order_by('id')

        paginator = ProductPagination()
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
            return Response({"error": "La categoría especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)
        if not all([name, description, price, category]):
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)
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