"""
 Define Model for Product Attributes.
"""

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, blank=False)
    category = models.CharField(max_length=255, blank=False)
    brand = models.CharField(max_length=255, blank=False)
    price = models.IntegerField(blank=False)
    stock = models.IntegerField(blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} of {self.category} category"
