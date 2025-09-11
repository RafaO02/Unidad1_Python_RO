from django.contrib import admin
from .models import Organization


# Register your models here.
from .models import Category, Zone, Device, Measurement, Alert, Product, ProductAlert

admin.site.register([Category, Zone, Measurement, Alert, Product, ProductAlert])

admin.site.register(Organization)

@admin.register(Device)
class DispositivoAdmin(admin.ModelAdmin):

    list_display = ("name", "category", "zone", "created_at", "update_at")
    list_filter = ("category", "zone")
    search_fields = ("name",)



