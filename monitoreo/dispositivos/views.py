from django.shortcuts import render, get_object_or_404
from .models import Device, Category, Alert, Measurement, Zone
from django.db.models import Count


def dashboard(request):
    categories = Category.objects.all()
    zones = Zone.objects.all()
    selected_category = request.GET.get('category', 'all')
    selected_zone = request.GET.get('zone', 'all')

    devices = Device.objects.all()
    if selected_category != 'all':
        devices = devices.filter(Category_id=selected_category)
    if selected_zone != 'all':
        devices = devices.filter(zone_id=selected_zone)

    # Contar dispositivos por categoría
    devices_by_category = Device.objects.values('Category__name').annotate(count=Count('id')).order_by('-count')
    
    # Contar dispositivos por zona
    devices_by_zone = Device.objects.values('zone__name').annotate(count=Count('id')).order_by('-count')
    
    # Contar alertas de la semana por severidad
    alert_count_by_severity = Alert.objects.filter(created_at__gte="2025-09-01").values('severity').annotate(count=Count('id'))

    # Últimas 10 mediciones
    latest_measurements = Measurement.objects.all().order_by('-recorded_at')[:10]

    # Últimas 5 alertas recientes
    recent_alerts = Alert.objects.select_related('measurement').order_by('-created_at')[:5]

    return render(request, 'dispositivos/dashboard.html', {
        'categories': categories,
        'zones': zones,
        'selected_category': selected_category,
        'selected_zone': selected_zone,
        'devices': devices,
        'devices_by_category': devices_by_category,
        'devices_by_zone': devices_by_zone,
        'alert_count_by_severity': alert_count_by_severity,
        'latest_measurements': latest_measurements,
        'recent_alerts': recent_alerts,  # <-- AGREGA ESTA LÍNEA
    })

def devices(request):
    selected_category = request.GET.get('category')
    selected_zone = request.GET.get('zone', 'all')
    categories = Category.objects.all()
    zones = Zone.objects.all()  # <-- AGREGA ESTA LÍNEA

    device_list = Device.objects.all()
    if selected_category and selected_category != 'all':
        device_list = device_list.filter(Category_id=selected_category)
    if selected_zone and selected_zone != 'all':
        device_list = device_list.filter(zone_id=selected_zone)

    return render(request, 'dispositivos/devices.html', {
        'devices': device_list,
        'categories': categories,
        'zones': zones,  # <-- AGREGA ESTA LÍNEA
        'selected_category': selected_category,
        'selected_zone': selected_zone,  # <-- AGREGA ESTA LÍNEA
    })

def device_detail(request, id):
    device = get_object_or_404(Device, pk=id)
    measurements = Measurement.objects.filter(id=id).order_by('-recorded_at')
    alerts = Alert.objects.filter(id=id).order_by('-created_at')
    return render(request, 'dispositivos/device_detail.html', {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    })

def measurements(request):
    measurements = Measurement.objects.select_related('device').order_by('-recorded_at')[:50]
    return render(request, 'dispositivos/measurements.html', {
        'measurements': measurements
    })

def measurement_detail(request, id):
    measurement = get_object_or_404(Measurement, pk=id)
    return render(request, 'dispositivos/measurements_detail.html', {
        'measurements': measurement
    })
