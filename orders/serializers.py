from rest_framework import serializers
from .models import Order
from products.serializers import ProductSerializer
from .models import OrderItem

class UserOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class UserOrderSerializer(serializers.ModelSerializer):
    items = UserOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "city",
            "pincode",
            "landmark",
            "payment_method",
            "items",
            "status",        
            "created_at",  
        ]
        read_only_fields = ["id"]