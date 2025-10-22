from django.db import models
from django.db.models import F, Sum
from .CategoryM import Category
from django.core.validators import RegexValidator

# Product Model

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=70,blank=False)
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        validators=[
            RegexValidator(
                regex=r'^(?!0+(?:\.0+)?$)\d+(?:\.\d+)?$',
                message="El precio debe ser un número positivo mayor que cero. Ej: 1000.00",
                code='invalid_price'
                         )]
    )
        
    
    stock = models.IntegerField(default=0, validators=[
        RegexValidator(
            regex=r'^(0|[1-9]\d*)$',
            message="El stock debe ser un número entero no negativo. Ej: 50",
            code='invalid_stock'
        )
    ])
    status = models.BooleanField(default="True")
    category = models.ManyToManyField('Category', related_name='products', blank=True) 
    
    @classmethod
    def calculateTotalStock(cls):
        total_stock = Product.objects.filter(status="1").annotate(
            totalProduct = F('price') * F('stock')
        ).aggregate(total_stock=Sum('totalProduct'))['total_stock'] or 0
        return total_stock if total_stock is not None else 0
    
    @classmethod
    def calculateTotalProducts(cls):
        total_products = Product.objects.filter(status="1").count()
        return total_products if total_products is not None else 0
 
    def returnCategoriesAsText(self):
      return ", ".join([category.name for category in self.category.all()])

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Valida el modelo antes de guardarlo
        super().save(*args, **kwargs)
  