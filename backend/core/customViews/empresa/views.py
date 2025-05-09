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
from ...models import ComprobantePago, ComprobantePagoFactura, Empresa
from decimal import Decimal


def allEmpresasData(request, organizacion_id):
    """
    Devuelve todas las empresas que pertenecen a la organización indicada,
    mostrando todos sus atributos relevantes, incluyendo una dirección completa.
    """
    empresas = Empresa.objects.select_related('UsoCfdi', 'regimenFiscal', 'organizacion') \
                              .filter(organizacion_id=organizacion_id)

    data = []
    for e in empresas:
        direccioncompleta = f"{e.calle} {e.numeroExterior or ''}, {e.colonia}, {e.codigoPostal}, {e.ciudad}, {e.estado}"

        data.append({
            "id": e.id,
            "numero": e.numero,
            "nombre": e.nombre,
            "rfc": e.rfc,
            "codigoPostal": e.codigoPostal,
            "ciudad": e.ciudad,
            "estado": e.estado,
            "colonia": e.colonia,
            "numeroExterior": e.numeroExterior,
            "calle": e.calle,
            "organizacion": e.organizacion.nombre,
            "direccioncompleta": direccioncompleta.strip(),
        })

    return JsonResponse(data, safe=False)
