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
from ...models import ComprobantePago, ComprobantePagoFactura
from decimal import Decimal

def allcomprobantepagodata(request, organizacion_id):
    """
    Vista que retorna los datos de comprobantes de pago y facturas asociadas
    filtrados por la organización a la que pertenece el cliente (a través del modelo Factura).
    """
    # Filtramos los registros a través de la relación:
    # Factura -> OrdenTrabajo -> Cotizacion -> Cliente -> Empresa -> organizacion_id
    comprobantes_facturas = ComprobantePagoFactura.objects.select_related(
        'comprobantepago',
        'factura',
    ).filter(
        factura__cotizacion__cliente__empresa__organizacion_id=organizacion_id
    )
    
    data = []
    for cpf in comprobantes_facturas:
        comprobante = cpf.comprobantepago
        factura = cpf.factura
        
        registro = {
            "folioComprobantePago": comprobante.id,
            "numeroComprobantePago": comprobante.numero,
            "folioFactura": factura.id,
            "numeroFactura": factura.numero,
            "fechaPago": comprobante.fechaPago,
            "montototal": cpf.montototal,
            "montopago": cpf.montopago,
            "montorestante": cpf.montorestante,
        }
        data.append(registro)
    
    return JsonResponse(data, safe=False)