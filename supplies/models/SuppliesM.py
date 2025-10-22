from django.db import models
from django.db.models import F, Sum
from supplies.models.SupplierM import Supplier
from django.core.validators import RegexValidator

class Supplies(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=70) 
    unitaryPrice = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[
                RegexValidator(
                regex=r'^(?!0+(?:\.0+)?$)\d+(?:\.\d+)?$',
                message="El precio unitario debe ser un número positivo mayor que cero. Ej: 1000.00",
                code='invalid_unitary_price'
            )]
    )
    stock = models.IntegerField(default=0, validators=[
        RegexValidator(
            regex=r'^(0|[1-9]\d*)$',
            message="El stock debe ser un número entero no negativo. Ej: 50",
            code='invalid_stock'
        )
    ])

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

    def save(self, *args, **kwargs):
        self.full_clean()  # Valida el modelo antes de guardarlo
        super().save(*args, **kwargs)