from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.http import JsonResponse
from ...models import Cotizacion, CotizacionServicio, OrdenTrabajo, OrdenTrabajoServicio, Cliente, Factura
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from ...models import Factura, OrdenTrabajoServicio, CotizacionServicio
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ...models import OrdenTrabajo, OrdenTrabajoServicio, PreCotizacion, PreCotizacionServicio
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from ...models import Factura, OrdenTrabajo, Cotizacion, OrdenTrabajoServicio, CotizacionServicio
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from ...models import PreCotizacion, PreCotizacionServicio
from ...models import ComprobantePago, ComprobantePagoFactura, Servicio
from decimal import Decimal

def allServiciosData(request, organizacion_id):
    """
    Devuelve todos los servicios que pertenecen a la organización indicada,
    mostrando sólo: codigo, nombre, metodo (descripcion) y precio.
    """
    # Seleccionamos también la relación 'metodos' para evitar consultas N+1
    servicios = Servicio.objects.select_related('metodos') \
                                .filter(organizacion_id=organizacion_id)

    data = []
    for s in servicios:
        data.append({
            "id": s.id,
            "numero": s.numero,                        # o s.id si tu modelo no tiene campo 'codigo'
            "nombreServicio": s.nombreServicio,
            "metodos": s.metodos.codigo,           # asumiendo que Metodos model tiene campo 'descripcion'
            "precio": str(s.precio),                   # convierte Decimal a string para JSON
        })

    return JsonResponse(data, safe=False)