from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Movement(models.Model):
    modifiedStock = models.IntegerField(validators=[MinValueValidator(0)]            
    )
    modificationType = models.CharField(max_length= 15) 
    dateHourCreation = models.DateTimeField(auto_now_add=True)
    dateHourUpdate = models.DateTimeField(auto_now=True)
    dateHourDeletion = models.DateTimeField(null=True, blank=True)
    comentary = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)


class SupplyMovement(Movement):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='supply_movements'
    )
    user_name = models.CharField(max_length=70, null=False, default='')

    supply = models.ForeignKey(
        'supplies.Supplies',
        on_delete=models.CASCADE,
        related_name='supply_movements'
    )

    supply_name = models.CharField(max_length=70, null=False , default='')

    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Movement {self.id} - Supply: {self.supply.name} - Type: {self.modificationType} - Modified Stock: {self.modifiedStock}"
    

class ProductMovement(Movement):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_movements'
    )
    user_name = models.CharField(max_length=70, null=False, default='')

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_movements'
    )
    
    product_name = models.CharField(max_length=70, null=False, default='')

    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Movement {self.id} - Product: {self.product.name} - Type: {self.modificationType} - Modified Stock: {self.modifiedStock}"
