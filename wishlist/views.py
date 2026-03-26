from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from products.models import Product
from .serializers import WishlistSerializer


class WishlistView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wishlist = Wishlist.objects.filter(user=request.user)

            serializer = WishlistSerializer(wishlist, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=500
            )



class AddToWishlist(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get("product_id")

            product = Product.objects.get(id=product_id)

            Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )

            return Response({"message": "Added to wishlist"})

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        except Exception:
            return Response({"error": "Something went wrong"}, status=500)

        
    




class RemoveWishlist(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            product_id = request.data.get("product_id")

            Wishlist.objects.filter(
                user=request.user,
                product_id=product_id
            ).delete()

            return Response({"message": "Removed"})
        except Exception as e:

            return Response(
                {"error": str(e)},
                status=500
            )
        