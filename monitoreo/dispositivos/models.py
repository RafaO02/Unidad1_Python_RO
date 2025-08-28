from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    DESCRIPCION = models.TextField(blank=True, null=True)


class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    consumo_maximo = models.IntegerField()
    estado = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Alerta(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name="alertas")
    tipo = models.CharField(max_length=50)  
    mensaje = models.CharField(max_length=255)
    umbral_w = models.DecimalField(max_digits=10, decimal_places=2)
    consumo_registrado_w = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)  
    reconocida = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.tipo}] {self.dispositivo.nombre} @ {self.creado_en:%Y-%m-%d %H:%M}"