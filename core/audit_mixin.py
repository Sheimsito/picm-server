# core/audit_mixin.py
from auditlog.context import set_actor

class AuditlogUserMixin:
  
    def perform_create(self, serializer):
        with set_actor(self.request.user):
            super().perform_create(serializer)

    def perform_update(self, serializer):
        with set_actor(self.request.user):
            super().perform_update(serializer)

    def perform_destroy(self, instance):
        with set_actor(self.request.user):
            instance.status = False
            instance.save()
