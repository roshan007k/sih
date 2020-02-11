from django.db import models
from datetime import datetime
# Create your models here.
class Product(models.Model):
    FoodGrains = 1
    CashCrops = 2
    PlantationCrops = 3
    HorticultureCrops = 4
    PRODUCT_TYPES = (
        (FoodGrains, 'Food'),
        (CashCrops, 'Cash'),
        (PlantationCrops, 'Plantation'),
        (HorticultureCrops, 'Horticulture'),
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='images/')
    product_type = models.PositiveSmallIntegerField(choices=PRODUCT_TYPES)

    timestamp = models.DateField(auto_now_add=True, auto_now=False)