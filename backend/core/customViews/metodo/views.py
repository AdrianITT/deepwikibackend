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
from ...models import ComprobantePago, ComprobantePagoFactura, Metodos
from decimal import Decimal

def allMetodosData(request, organizacion_id):
    """
    Devuelve todos los métodos que pertenecen a la organización indicada,
    mostrando sólo: numero (ID) y código.
    """
    metodos = Metodos.objects.filter(organizacion_id=organizacion_id)

    data = [
        {
            "id": m.id,
            "numero": m.numero,
            "codigo": m.codigo,
        }
        for m in metodos
    ]

    return JsonResponse(data, safe=False)
    
