from django.db import models


#-----------------------------------------------
#   Modelo Base con Atributos Comunes
#-----------------------------------------------

class BaseModel(models.Model):
    ESTADO =[
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    estado = models.CharField(max_length=10, choices=ESTADO, default='ACTIVO')
    created_at = models.DateTimeField(auto_now_add=True) # se asigna al crear
    update_at = models.DateTimeField(auto_now=True) # se actualiza al guardar
    deleted_at = models.DateTimeField(null=True, blank=True) # se asigna al eliminar

    class Meta:
        abstract = True # no crea tabla, solo se hereda


#-----------------------------------------------
#   tablas principales
#-----------------------------------------------

class Organization(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    
class User(BaseModel):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.username
    
class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Zone(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='zones')

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='products')

    def __str__(self):
        return f"{self.brand} {self.model}"

class Device(BaseModel):
    name = models.CharField(max_length=100)
    max_consumption_w = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="devices", blank=True, null=True)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="devices", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE , related_name='devices')
    Category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="devices", blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["Product"]),
            models.Index(fields=["zone"]),
            models.Index(fields=["organization"]),
            models.Index(fields=["Category"]),
        ]

class Measurement(BaseModel):
 
    recorded_at = models.DateTimeField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    device = models.ForeignKey(Device, on_delete=models.CASCADE , related_name='measurements')
    def __str__(self):
        return f"{self.device.name} - {self.recorded_at}"
    
class Alert(BaseModel):
    SEVERITY_CHOICES = [
        ('grave', 'Grave'),
        ('alto', 'Alto'),
        ('mediano', 'Mediano'),
        ('bajo', 'Bajo'),
    ]
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='alerts')
    type = models.CharField(max_length=50)
    registered_consumption_w = models.DecimalField(max_digits=10, decimal_places=2)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    recognized = models.BooleanField(default=False)
    treashold_w = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Alert {self.severity} at {self.created_at}"

class ProductAlert(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_alerts')
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='product_alerts')

    class Meta:
        unique_together = ('product', 'alert')