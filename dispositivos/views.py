from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Alert
from .models import Device
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CompanyRegistrationForm,PasswordResetForm
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your views here.
# views.py



def inicio(request):
    dispositivos = Device.objects.select_related("categoria")  # join
    return render(request, "dispositivos/inicio.html", {"dispositivos": dispositivos})



def dashboard(request):
    # Filtrar las alertas de la semana
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_alerts = Alert.objects.filter(fecha_generada__gte=one_week_ago)

    # Conteo de alertas por severidad
    grave_count = recent_alerts.filter(severidad='Grave').count()
    alto_count = recent_alerts.filter(severidad='Alto').count()
    mediano_count = recent_alerts.filter(severidad='Mediano').count()

    # Lista corta de alertas recientes (las últimas 5)
    recent_alerts_list = recent_alerts.order_by('-fecha_generada')[:5]

    context = {
        'grave_count': grave_count,
        'alto_count': alto_count,
        'mediano_count': mediano_count,
        'recent_alerts_list': recent_alerts_list,
    }

    return render(request, 'dispositivos/dashboard.html', context)

def all_alerts(request):
    one_week_ago = timezone.now() - timedelta(days=7)
    alerts = Alert.objects.filter(fecha_generada__gte=one_week_ago).order_by('-fecha_generada')

    context = {
        'alerts': alerts
    }

    return render(request, 'dispositivos/all_alerts.html', context)  # Verifica que el nombre del template sea correcto

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            # Guardar el usuario y la empresa
            user = form.save()
            company_name = form.cleaned_data.get('company_name')
            # Mostrar mensaje de éxito
            messages.success(request, f"¡Registro exitoso! {company_name} ha sido registrada.")
            return redirect('login')  # Redirigir al login después de registrar
    else:
        form = CompanyRegistrationForm()

    return render(request, 'dispositivos/register.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Simulamos el envío del correo de recuperación
            send_mail(
                'Recuperación de Contraseña',
                'Por favor, sigue este enlace para restablecer tu contraseña: http://example.com/reset-password',
                'no-reply@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Se han enviado instrucciones a tu correo electrónico para recuperar tu contraseña.")
            return redirect('login')  # Redirige al login después de enviar las instrucciones
    else:
        form = PasswordResetForm()

    return render(request, 'dispositivos/password_reset.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirige al dashboard después de iniciar sesión
            else:
                messages.error(request, "Credenciales inválidas")
        else:
            messages.error(request, "Por favor, ingresa los datos correctamente.")
    else:
        form = LoginForm()

    # Verificar si se pasa un mensaje de éxito después de la recuperación o registro
    if 'password_reset' in request.GET:
        messages.success(request, "Se han enviado instrucciones a tu correo electrónico para recuperar tu contraseña.")
    elif 'registered' in request.GET:
        messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")

    return render(request, 'dispositivos/login.html', {'form': form})


