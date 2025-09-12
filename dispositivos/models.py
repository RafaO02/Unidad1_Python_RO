from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    company_name = models.CharField(max_length=255, null=True, blank=True)  

    
    groups = models.ManyToManyField(
        Group,
        through='CustomUser_groups',  
        related_name='customuser_set',  
    )

    def __str__(self):
        return self.username  
class CustomUser_groups(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'dispositivos_customuser_groups' 

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"  

# Modelo de Organización
class Organization(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Categoría
class Category(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Producto
class Product(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Zona
class Zone(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre

# Modelo de Dispositivo
class Device(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    numero_serie = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Dispositivo {self.numero_serie}"

    class Meta:
        indexes = [
            models.Index(fields=["categoria"]),
            models.Index(fields=["zone"]),
        ]

# Modelo de Alerta
class Alert(models.Model):
    dispositivo = models.ForeignKey(Device, on_delete=models.CASCADE)
    severidad = models.CharField(max_length=50)
    mensaje = models.TextField()
    fecha_generada = models.DateTimeField()
    estado = models.CharField(max_length=50)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.severidad}] {self.dispositivo.numero_serie} @ {self.creado_en:%Y-%m-%d %H:%M}"

# Modelo de Medición
class Measurement(models.Model):
    dispositivo = models.ForeignKey(Device, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=50)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    eliminado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Medición {self.id} - {self.fecha_registro} - {self.dispositivo.numero_serie}"