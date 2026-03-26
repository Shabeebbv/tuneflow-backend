from django.db import models
from accounts.models import UserProfile
from products.models import Product
from django.conf import settings

class CartItem(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"