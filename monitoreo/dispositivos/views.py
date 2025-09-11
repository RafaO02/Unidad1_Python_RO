from django.shortcuts import render
from .models import Device, Alert, Measurement
from django.db.models import Count

def dashboard(request):
    # Contar dispositivos por categoría
    devices_by_category = Device.objects.values('category__name').annotate(count=Count('id')).order_by('-count')
    
    # Contar dispositivos por zona
    devices_by_zone = Device.objects.values('zone__name').annotate(count=Count('id')).order_by('-count')
    
    # Contar alertas de la semana por severidad
    alert_count_by_severity = Alert.objects.filter(created_at__gte="2025-09-01").values('severity').annotate(count=Count('id'))

    # Últimas 10 mediciones
    latest_measurements = Measurement.objects.all().order_by('-recorded_at')[:10]

    return render(request, 'dashboard.html', {
        'devices_by_category': devices_by_category,
        'devices_by_zone': devices_by_zone,
        'alert_count_by_severity': alert_count_by_severity,
        'latest_measurements': latest_measurements
    })
