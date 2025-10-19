from django.db import models
from django.db.models import F, Sum
from django.core.validators import RegexValidator


# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    nit = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{7,10}-\d{1}$',
                message="El NIT debe tener entre 7 y 10 dígitos seguidos de un guion y un dígito verificador. Ej: 900123456-7",
                code='invalid_nit'
            )
        ]
    )
    phone = models.CharField(
        unique= True,
        validators=[
            RegexValidator(
                regex= r'^(60[1245678]\d{7}|\d{7})$',
                message = "El teléfono debe iniciar con 60 y luego 8 dígitos extra. Ej: 6012345678",
                code= 'invalid_tel'
            )
        ],
            max_length= 10
    )
    email = models.EmailField(
            unique=True,
            error_messages={
                "unique": "Este correo ya está registrado",
                "invalid": "El correo ingresado no es válido, Ej: nombre@dominio.extension"
            }                                
        )  
    address = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
