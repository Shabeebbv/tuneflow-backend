from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            products = Product.objects.all()

            #  Existing search
            search = request.GET.get("search")

            #  NEW FILTERS
            brand = request.GET.get("brand")
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")

            #  SEARCH FILTER
            if search:
                products = products.filter(
                    Q(name__icontains=search) |
                    Q(category__icontains=search) |
                    Q(description__icontains=search)
                )

            #  BRAND FILTER
            if brand:
                products = products.filter(category__iexact=brand)

            #  PRICE FILTER
            if min_price:
                products = products.filter(price__gte=min_price)

            if max_price:
                products = products.filter(price__lte=max_price)

            #  PAGINATION (keep same)
            paginator = PageNumberPagination()
            paginator.page_size = 10

            paginated_products = paginator.paginate_queryset(products, request)

            serializer = ProductSerializer(paginated_products, many=True)

            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response(
                {'error': 'something went wrong', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        



    
class ProductDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, pk):
        try:

            product = Product.objects.get(id=pk)

            serializer = ProductSerializer(product)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'Error':'Product Not Found'},status=status.HTTP_404_NOT_FOUND
                            )
        except Exception as e:
            return Response({
                'error':'something went wrong','details':str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        