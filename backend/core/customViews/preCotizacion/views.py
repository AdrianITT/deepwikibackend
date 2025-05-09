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

def allPrecotizacionData(request, organizacion_id):
    precotizaciones = PreCotizacion.objects.select_related(
        'estado'
    ).filter(organizacion_id=organizacion_id)

    data = []

    for precotizacion in precotizaciones:
        nombreCompletoCliente = f"{precotizacion.nombreCliente} {precotizacion.apellidoCliente}"

        data.append({
            "precotizacionId": precotizacion.id,
            "numero": precotizacion.numero,
            "nombreCliente": nombreCompletoCliente,
            "nombreEmpresa": precotizacion.nombreEmpresa,
            "estado": {
                "estadoId": precotizacion.estado.id,
                "nombre": precotizacion.estado.nombre
            }
        })

    return JsonResponse(data, safe=False)

def detallePreCotizacionData(request, precotizacion_id):
    precotizacion = get_object_or_404(PreCotizacion, id=precotizacion_id)
    
    nombre_cliente = f"{precotizacion.nombreCliente} {precotizacion.apellidoCliente}"
    precotizacion_servicios = PreCotizacionServicio.objects.filter(preCotizacion=precotizacion)

    servicios = {}
    subtotal = 0

    for ps in precotizacion_servicios:
        precio = ps.precio
        cantidad = ps.cantidad
        subtotal_servicio = round(precio * cantidad, 2)
        subtotal += subtotal_servicio

        # Agrupar por id de PreCotizacionServicio
        servicios[ps.id] = {
            "servicioId": ps.servicio.id,
            "servicioNombre": ps.servicio.nombreServicio,
            "descripcion": ps.descripcion,
            "precio": f"{precio:.2f}",
            "cantidad": cantidad,
            "subtotal": f"{subtotal_servicio:.2f}"
        }

    # Cálculos
    descuento = precotizacion.descuento or 0
    valor_descuento = round(subtotal * descuento / 100, 2)
    subtotal_descuento = round(subtotal - valor_descuento, 2)

    iva_porcentaje = precotizacion.iva.porcentaje if precotizacion.iva else 0
    iva_decimal = iva_porcentaje
    iva_valor = round(subtotal_descuento * iva_decimal, 2)

    importe = round(subtotal_descuento + iva_valor, 2)

    # Si la cotización tiene tipoMoneda id = 2, realizamos la conversión por tipoCambioDolar
    if precotizacion.tipoMoneda.id == 2:
        tipoCambioDolar = precotizacion.organizacion.infoSistema.tipoCambioDolar
        subtotal = round(subtotal / tipoCambioDolar, 2)
        valor_descuento = round(valor_descuento / tipoCambioDolar, 2)
        subtotal_descuento = round(subtotal_descuento / tipoCambioDolar, 2)
        iva_valor = round(iva_valor / tipoCambioDolar, 2)
        importe = round(importe / tipoCambioDolar, 2)

    data = {
        "idPreCotizacion": precotizacion.id,
        "numero": precotizacion.numero,
        "empresa": {
            "nombre": precotizacion.nombreEmpresa,
            "denominacion": precotizacion.denominacion
        },
        "cliente": {
            "nombreCompleto": nombre_cliente,
            "correo": precotizacion.correo,
            "nombrePila": precotizacion.nombreCliente,
            "apPaterno": precotizacion.apellidoCliente,
        },
        "estado": {
            "id": precotizacion.estado.id,
            "nombre": precotizacion.estado.nombre
        },
        "tipoMoneda": {
            "id": precotizacion.tipoMoneda.id,
            "codigo": precotizacion.tipoMoneda.codigo,
            "descripcion": precotizacion.tipoMoneda.descripcion
        },
        "iva": {
            "id": precotizacion.iva.id,
            "porcentaje": f"{iva_decimal:.2f}"
        },
        "organizacion": {
            "id": precotizacion.organizacion.id,
            "nombre": precotizacion.organizacion.nombre
        },
        "fechaSolicitud": precotizacion.fechaSolicitud.strftime("%d-%m-%Y") if precotizacion.fechaSolicitud else "",
        "fechaCaducidad": precotizacion.fechaCaducidad.strftime("%d-%m-%Y") if precotizacion.fechaCaducidad else "",
        "descuento": str(descuento),
        "precotizacionservicios": [
            {  # Por cada servicio, lo englobamos con su id
                f"precotizacionservicioId": ps.id,
                **servicios[ps.id]
            } for ps in precotizacion_servicios
        ],
        "valores": {
            "subtotal": f"{subtotal:.2f}",
            "descuento": str(descuento),
            "valorDescuento": f"{valor_descuento:.2f}",
            "subtotalDescuento": f"{subtotal_descuento:.2f}",
            "iva": f"{iva_decimal:.2f}",
            "ivaValor": f"{iva_valor:.2f}",
            "importe": f"{importe:.2f}"
        }
    }

    return JsonResponse(data, safe=False)
