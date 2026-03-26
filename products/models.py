from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    old_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(null=True)
    ratings_count = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    image = models.URLField()
    description = models.TextField()
    tag = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name