from django.db import models
from django.db.models import F, Sum
from django.core.validators import MinValueValidator
from supplies.models.SupplierM import Supplier

class Supplies(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=30) 
    unitaryPrice = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE,
        related_name='supplies'
    )

    @classmethod
    def calculate_total_inventory_value(cls):
        return cls.objects.filter(status=True).annotate(
            totalSupply=F('unitaryPrice') * F('stock')
        ).aggregate(total_stock=Sum('totalSupply'))['total_stock'] or 0

    @classmethod
    def calculate_total_supplies(cls):
        return cls.objects.filter(status=True).count() or 0

    def __str__(self):
        return self.name
