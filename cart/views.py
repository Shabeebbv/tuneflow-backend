from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem
from products.models import Product
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated

class AddToCartView(APIView):
     permission_classes = [IsAuthenticated]
     def post(self, request):
        try:
            user = request.user
            product_id = request.data.get("product_id")

            product = Product.objects.get(id=product_id)

            cart_item, created = CartItem.objects.get_or_create(
                user=user,
                product=product
            )

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            serializer = CartSerializer(cart_item)

            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=500)
    


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user

            cart_items = CartItem.objects.filter(user=user)

            serializer = CartSerializer(cart_items, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=500)
    


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            product_id = request.data.get("product_id")

            CartItem.objects.filter(
                user=user,
                product_id=product_id
            ).delete()

            return Response({"message": "removed"})

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=500)
    



class UpdateCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            product_id = request.data.get("product_id")
            action = request.data.get("action")

            cart_item = CartItem.objects.get(
                user=user,
                product_id=product_id
            )

            if action == "increase":
                if cart_item.quantity < 5:
                    cart_item.quantity += 1

            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1

            cart_item.save()

            return Response({"message": "updated", "quantity": cart_item.quantity})

        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=404)

        except Exception as e:
            return Response({"error": "Something went wrong", "details": str(e)}, status=500)