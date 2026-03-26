from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem
from cart.models import CartItem
from .serializers import UserOrderSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user

            cart_items = CartItem.objects.filter(user=user)

            if not cart_items.exists():
                return Response(
                    {"error": "Cart is empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = UserOrderSerializer(data=request.data)

            if serializer.is_valid():

                order = serializer.save(user=user)

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

                cart_items.delete()

                return Response(
                    {"message": "Order created"},
                    status=status.HTTP_201_CREATED
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user

            orders = Order.objects.filter(user=user)

            serializer = UserOrderSerializer(orders, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
