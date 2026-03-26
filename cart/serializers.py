from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]