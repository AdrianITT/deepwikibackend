from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.http import JsonResponse
from ...models import Cotizacion, CotizacionServicio, OrdenTrabajo, OrdenTrabajoServicio, Cliente, Factura
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from ...models import Factura, OrdenTrabajoServicio, CotizacionServicio, FacturaServicio
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

def allfacturasdata(request, organizacion_id):
    # Traemos las facturas vinculadas a una cotización cuya empresa pertenece a la organización
    facturas = (
        Factura.objects
        .select_related('cotizacion__cliente__empresa')
        .filter(cotizacion__cliente__empresa__organizacion_id=organizacion_id)
    )

    data = []
    for factura in facturas:
        cotizacion = factura.cotizacion
        cliente = cotizacion.cliente
        empresa = cliente.empresa

        # Nombre completo del cliente
        nombre_completo = f"{cliente.nombrePila} {cliente.apPaterno}"
        if cliente.apMaterno:
            nombre_completo += f" {cliente.apMaterno}"

        data.append({
            "id": factura.id,
            "folio": factura.numero,
            "numeroCotizacion": cotizacion.numero,
            "cliente": nombre_completo,
            "empresa": empresa.nombre,
            "fechaExpedicion": factura.fechaExpedicion,
        })

    return JsonResponse(data, safe=False)

def detalleFacturaData(request, factura_id):
    # 1) Traer la factura con sus relaciones necesarias
    try:
        factura = Factura.objects.select_related(
            'cotizacion__cliente__empresa__organizacion__infoSistema',
            'formaPago',
            'metodoPago',
        ).get(id=factura_id)
    except Factura.DoesNotExist:
        raise Http404("Factura no encontrada")

    cotizacion   = factura.cotizacion
    cliente      = cotizacion.cliente
    empresa      = cliente.empresa
    organizacion = empresa.organizacion

    # 2) Nombre completo del contacto
    nombreCompleto = f"{cliente.nombrePila} {cliente.apPaterno}"
    if cliente.apMaterno:
        nombreCompleto += f" {cliente.apMaterno}"

    # 3) Factor de descuento de la factura
    pct_factura   = Decimal(factura.porcentaje or 0)
    factor_factura = (Decimal(100) - pct_factura) / Decimal(100)

    # 4) Recoger los ítems de la factura
    fs_qs = FacturaServicio.objects.select_related('servicio__metodos')\
                                   .filter(factura=factura)

    servicios_list = []
    subtotal = Decimal("0")
    for fs in fs_qs:
        # 4.1) Aplicar descuento de factura sobre el precio unitario
        precio_desc = (Decimal(fs.precio) * factor_factura).quantize(Decimal("0.01"))

        # 4.2) Subtotal de línea
        linea_sub = (precio_desc * fs.cantidad).quantize(Decimal("0.01"))
        subtotal += linea_sub

        servicios_list.append({
            "facturaServicioId": fs.id,
            "cantidad":          fs.cantidad,
            "descripcion":       fs.descripcion,
            "precioUnitario":    str(precio_desc),
            "subtotal":          str(linea_sub),
            "servicio": {
                "id":     fs.servicio.id,
                "nombre": fs.servicio.nombreServicio,
                "metodo": {
                    "id":     fs.servicio.metodos.id,
                    "codigo": fs.servicio.metodos.codigo,
                }
            }
        })

    # 5) Cálculos de descuento de la cotización e IVA
    pct_cot = Decimal(cotizacion.descuento or 0)
    val_desc = (subtotal * pct_cot / Decimal(100)).quantize(Decimal("0.01"))
    subcDesc = (subtotal - val_desc).quantize(Decimal("0.01"))

    iva_pct = Decimal(cotizacion.iva.porcentaje or 0)
    iva_val = (subcDesc * iva_pct).quantize(Decimal("0.01"))

    total = (subcDesc + iva_val).quantize(Decimal("0.01"))

    # 6) Montar el JSON de salida
    data = {
        "id":               factura.id,
        "numerofactura":    factura.numero,
        "idcotizacion":   cotizacion.id,
        "numerocotizacion": cotizacion.numero,
        "fecha":            factura.fechaExpedicion,
        "porcentajeFactura": str(pct_factura),
        "formaPago":        factura.formaPago.descripcion if factura.formaPago else "",
        "metodoPago":       factura.metodoPago.codigo      if factura.metodoPago else "",
        "monedaCodigo":     cotizacion.tipoMoneda.codigo   if cotizacion.tipoMoneda else "",
        "monedaDesc":       cotizacion.tipoMoneda.descripcion if cotizacion.tipoMoneda else "",
        "ordenCompra":      factura.ordenCompra,
        "empresa":          empresa.nombre,
        "rfcEmpresa":       getattr(empresa, 'rfc', ''),
        "contacto":         nombreCompleto,
        "correo":           cliente.correo,
        "servicios":        servicios_list,
        "valores": {
            "subtotal":            str(subtotal),
            "descuentoCotizacion": str(pct_cot),
            "valorDescuento":      str(val_desc),
            "subtotalDesc":        str(subcDesc),
            "ivaPct":              str(iva_pct),
            "ivaValor":            str(iva_val),
            "totalFinal":          str(total),
        }
    }

    return JsonResponse(data, safe=False)

def facturaCliente(request, factura_id):
    """
    Retorna el id del cliente, su nombre completo y el id de la factura.
    Se obtiene la factura a partir del identificador recibido y se accede
    al cliente asociado vía Cotizacion.
    """
    # 1) Traer factura junto con la cotización → cliente
    factura = get_object_or_404(
        Factura.objects.select_related('cotizacion__cliente'),
        id=factura_id
    )
    cliente = factura.cotizacion.cliente

    # 2) Construir nombre completo
    nombre_completo = f"{cliente.nombrePila} {cliente.apPaterno}"
    if cliente.apMaterno:
        nombre_completo += f" {cliente.apMaterno}"

    # 3) Armar y devolver JSON
    data = {
        "factura_id":    factura.id,
        "numerofactura": factura.numero,
        "cliente_id":    cliente.id,
        "numerocliente": cliente.numero,
        "nombreCompleto": nombre_completo,
    }
    return JsonResponse(data)

def facturaMontoTotal(request, factura_id):
    """
    Vista que retorna la información de una factura y el montoTotal del último ComprobantePagoFactura asociado.
    
    Parámetros:
      - factura_id: Identificador de la factura.
    
    Retorna un JSON con:
      - id: El identificador de la factura.
      - tipoMoneda: El tipo de moneda de la factura.
      - montoTotal: El valor de 'montorestante' del último registro insertado en ComprobantePagoFactura que corresponda a la factura.
    """
    try:
        # Se obtiene la factura a partir del id
        factura = Factura.objects.get(id=factura_id)
    except Factura.DoesNotExist:
        return JsonResponse({"error": "Factura no encontrada"}, status=404)
    
    # Filtramos los registros en ComprobantePagoFactura asociados a la factura,
    # y ordenamos de forma descendente por 'id' para obtener el último insertado.
    comprobante_pago_factura = ComprobantePagoFactura.objects.filter(
        factura=factura
    ).order_by('-id').first()
    
    # Si se encontró el registro, asignamos el montorestante a monto_total.
    monto_total = comprobante_pago_factura.montorestante if comprobante_pago_factura else None
    
    data = {
        "id": factura.id,
        "tipoMoneda": factura.tipoMoneda,
        "montoTotal": monto_total
    }
    
    return JsonResponse(data)
