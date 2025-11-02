from django.db import models
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog

# Category Model

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    description = models.CharField(max_length=70,blank=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

history = AuditlogHistoryField()
auditlog.register(Category)
