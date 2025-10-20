from django.db import models


# Category Model

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    description = models.CharField(max_length=70,blank=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name