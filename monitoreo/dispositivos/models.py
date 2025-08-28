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
