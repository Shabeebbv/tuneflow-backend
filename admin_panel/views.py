from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer,ProductSerializer,AdminOrderSerializer 
from accounts.models import UserProfile
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from products.models import Product
from .permissions import IsAdminUser
from orders.models import Order
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.db.models import Sum,Q


class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=400)

        if user.role != "admin":
            return Response({"error": "Not an admin"}, status=403)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "email": user.email,
                "role": user.role
            }
        })
    

class UserListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = UserProfile.objects.filter(is_deleted=False)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class UserDetailView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class ToggleUserStatus(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.status = "inactive" if user.status == "active" else "active"
        user.save()

        return Response({
            "message": "Status updated",
            "status": user.status
        })
    

class DeleteUser(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.is_deleted = True
        user.save()
        return Response({"message": "User moved to trash"})
    

class DeletedUserListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = UserProfile.objects.filter(is_deleted=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    
    

class RestoreUser(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            user = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.is_deleted = False
        user.save()

        return Response({"message": "User restored"})
    
    
    
#product


class ProductCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    
    
    def get(self, request):
        products = Product.objects.all()

        search = request.GET.get("search")

        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(category__icontains=search)
            )

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result, many=True)

        return paginator.get_paginated_response(serializer.data)

# class ProductListView(APIView):
#     permission_classes = [IsAdminUser]

   

class ProductUpdateView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    

class ProductDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        product.delete()
        return Response({"message": "Product deleted"})
 
 
 #order

class OrderListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all().order_by("-id")
        serializer = AdminOrderSerializer(orders, many=True)
        return Response(serializer.data)
    

class OrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = AdminOrderSerializer(order)
        return Response(serializer.data)
    
class UpdateOrderStatus(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        status_value = request.data.get("status").lower()

        if status_value not in ["pending", "shipped", "delivered","cancelled"]:
            return Response({"error": "Invalid status"}, status=400)

        order.status = status_value
        order.save()

        return Response({
            "message": "Order status updated",
            "status": order.status
        })
    


# class RevenueView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         total = Order.objects.aggregate(total=Sum("total_price"))
#         return Response(total)
    
    

class OrderCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = Order.objects.count()
        return Response({"total_orders": count})
    

class OrdersByCategory(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {}

        orders = Order.objects.all()

        for order in orders:
            for item in order.items.all():
                category = item.product.category
                data[category] = data.get(category, 0) + 1

        result = [{"name": k, "value": v} for k, v in data.items()]
        return Response(result)
    


class MonthlySalesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            data = (
                Order.objects
                .annotate(month=ExtractMonth("created_at"))
                .values("month")
                .annotate(total=Sum("items__price"))  # ✅ FIXED
                .order_by("month")
            )

            result = [
                {
                    "month": item["month"],
                    "sales": float(item["total"] or 0)
                }
                for item in data
            ]

            return Response(result)

        except Exception as e:
            return Response({"error": str(e)}, status=500)