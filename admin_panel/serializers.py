from rest_framework import serializers
from accounts.models import UserProfile   
from products.models import Product
from orders.models import Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "email", "name", "role", "status"]



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class AdminOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "image": obj.product.image,
            "price": str(obj.product.price),
        }


class AdminOrderSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source="user.name")

    class Meta:
        model = Order
        fields = ["id", "user_name", "status", "items", "created_at"]