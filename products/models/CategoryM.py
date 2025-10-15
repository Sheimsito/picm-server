from django.db import models


# Category Model

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=False)

    def __str__(self):
        return self.name