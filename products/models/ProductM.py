from django.db import models
from django.db.models import F, Sum
from .CategoryM import Category

# Product Model

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.IntegerField(default=0)
    status = models.BooleanField(max_length=20, default="True")
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
    
  