from django.shortcuts import render

# Create your views here.
def inicio (request):
    dispositivos =[
        {"Nombre":"Sensor temperatura","consumo":50},
        {"Nombre":"Medidor Solar","consumo":120},
        {"Nombre":"Sensor Movimiento","consumo":30},
        {"Nombre":"Calefactor","consumo":200},
    ]

    consumo_maximo = 100

    return render(request, "dispositivos/inicio.html",{
        "dispositivos": dispositivos,
        "consumo_maximo": consumo_maximo
    })
