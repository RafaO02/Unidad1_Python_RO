from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)  # antes DESCRIPCION

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    # consumo máximo en Watts (Decimal según ERD)
    consumo_maximo_w = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.BooleanField(default=True)

    # Relaciones (1→N): una categoría/zona tiene muchos dispositivos
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="dispositivos"
    )
    zona = models.ForeignKey(
        Zona, on_delete=models.PROTECT, related_name="dispositivos"
    )

    def __str__(self):
        return self.nombre

    class Meta:  # índices útiles para filtros frecuentes
        indexes = [
            models.Index(fields=["categoria"]),
            models.Index(fields=["zona"]),
        ]


class Alerta(models.Model):
    dispositivo = models.ForeignKey(
        Dispositivo, on_delete=models.CASCADE, related_name="alertas"
    )
    tipo = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=255)
    umbral_w = models.DecimalField(max_digits=10, decimal_places=2)
    consumo_registrado_w = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)
    reconocida = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.tipo}] {self.dispositivo.nombre} @ {self.creado_en:%Y-%m-%d %H:%M}"
