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
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ...models import Cotizacion, CotizacionServicio, CertificadoSelloDigital
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ...models import (
    Cotizacion,
    CotizacionServicio,
    CertificadoSelloDigital,
)

def duplicarCotizacion(request, cotizacion_id):
    original = get_object_or_404(Cotizacion, id=cotizacion_id)

    cliente_id = request.GET.get('cliente')
    if cliente_id:
        try:
            nuevo_cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            return HttpResponseBadRequest("Cliente no encontrado")
    else:
        nuevo_cliente = original.cliente

    # Crear la nueva cotización
    nueva_cotizacion = Cotizacion.objects.create(
        denominacion=original.denominacion,
        fechaSolicitud=timezone.now().date(),
        fechaCaducidad=timezone.now().date() + timedelta(days=30),
        descuento=original.descuento,
        iva=original.iva,
        estado=original.estado,
        cliente=nuevo_cliente,
        tipoMoneda=original.tipoMoneda,
    )

    # Copiar los servicios asociados
    cotizacion_servicios = CotizacionServicio.objects.filter(cotizacion=original)
    for cs in cotizacion_servicios:
        CotizacionServicio.objects.create(
            descripcion=cs.descripcion,
            precio=cs.precio,
            cotizacion=nueva_cotizacion,
            servicio=cs.servicio,
            cantidad=cs.cantidad,
        )

    return JsonResponse({
        "mensaje": "Cotización duplicada exitosamente",
        "nueva_cotizacion_id": nueva_cotizacion.id,
        "nuevo_cliente": f"{nuevo_cliente.nombrePila} {nuevo_cliente.apPaterno}",
    })

def allcotizacionesdata(request, organizacion_id):
    #permission_classes = [IsAuthenticated]
    cotizaciones = Cotizacion.objects.select_related(
        'cliente__empresa', 
        'estado', 
        'tipoMoneda'
    ).filter(cliente__empresa__organizacion_id=organizacion_id)

    data = []
    for cot in cotizaciones:
        # Armamos el nombre completo del contacto (cliente)
        nombre_completo = f"{cot.cliente.nombrePila} {cot.cliente.apPaterno}"
        if cot.cliente.apMaterno:
            nombre_completo += f" {cot.cliente.apMaterno}"

        data.append({
            "Cotización": cot.id,
            "numero": cot.numero,
            "Empresa": cot.cliente.empresa.nombre,
            "division": cot.cliente.division if cot.cliente.division else "No aplica",
            "Contacto": nombre_completo,
            "Correo": cot.cliente.correo,
            "CodigoPostal": cot.cliente.codigoPostalCliente,
            "CalleEmpresa": cot.cliente.empresa.calle,
            "rfcEmpresa": cot.cliente.empresa.rfc,
            "Solicitud": cot.fechaSolicitud,
            "Expiración": cot.fechaCaducidad,
            "Moneda": {
                "id": cot.tipoMoneda.id,
                "codigo": cot.tipoMoneda.codigo,
                "descripcion": cot.tipoMoneda.descripcion,
            },
            "Estado": {
                "id": cot.estado.id,
                "nombre": cot.estado.nombre,
            },
            "Organizacion": cot.cliente.empresa.organizacion.id,
        })

    return JsonResponse(data, safe=False)

def detalleCotizacionData(request, cotizacion_id):
    #permission_classes = [IsAuthenticated]
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    cliente = cotizacion.cliente
    empresa = cliente.empresa
    organizacion = empresa.organizacion

    direccionCliente = {
        "calle": cliente.calleCliente,
        "numero": cliente.numeroCliente,
        "colonia": cliente.coloniaCliente,
        "ciudad": cliente.ciudadCliente,
        "estado": cliente.estadoCliente,
        "codigoPostal": cliente.codigoPostalCliente
    }

    direccionEmpresa = {
        "calle": empresa.calle,
        "numero": empresa.numero,
        "colonia": empresa.colonia,
        "ciudad": empresa.ciudad,
        "estado": empresa.estado,
        "codigoPostal": empresa.codigoPostal
    }

    # Obtenemos los servicios de la cotización y calculamos el subtotal
    cotizacionServicios = CotizacionServicio.objects.filter(cotizacion=cotizacion)
    subtotal = sum(cs.precio * cs.cantidad for cs in cotizacionServicios)

    # Se asume que el descuento es un porcentaje, por ejemplo 5 para un 5%
    descuentoPorcentaje = cotizacion.descuento  
    valorDescuento = subtotal * descuentoPorcentaje / 100
    subtotalDescuento = subtotal - valorDescuento

    # Calculo del IVA (se asume que el porcentaje está en formato entero, p.ej. 16 para 16%)
    ivaPorcentaje = cotizacion.iva.porcentaje
    subtotalDescuento = Decimal(str(subtotalDescuento))
    ivaValor = subtotalDescuento * ivaPorcentaje

    # Importe final
    importe = subtotalDescuento + ivaValor

    # Si la cotización tiene el tipoMoneda id = 2, se realiza la conversión dividiendo por tipoCambioDolar
    if cotizacion.tipoMoneda.id == 2:
        tipoCambioDolar = organizacion.infoSistema.tipoCambioDolar
        subtotal = subtotal / tipoCambioDolar
        valorDescuento = valorDescuento / tipoCambioDolar
        subtotalDescuento = subtotalDescuento / tipoCambioDolar
        ivaValor = ivaValor / tipoCambioDolar
        importe = importe / tipoCambioDolar

    # Redondear valores a 2 decimales
    subtotal = round(subtotal, 2)
    valorDescuento = round(valorDescuento, 2)
    subtotalDescuento = round(subtotalDescuento, 2)
    ivaValor = round(ivaValor, 2)
    importe = round(importe, 2)

    data = {
        "idCotizacion": cotizacion.id,
        "numero":cotizacion.numero,
        "cliente": {
            "nombreCompleto": f"{cliente.nombrePila} {cliente.apPaterno} {cliente.apMaterno}",
            "correo": cliente.correo,
            "direccion": direccionCliente
        },
        "empresa": {
            "nombre": empresa.nombre,
            "direccion": direccionEmpresa
        },
        "estado": {
            "id": cotizacion.estado.id,
            "nombre": cotizacion.estado.nombre,
        },
        "fechaSolicitada": cotizacion.fechaSolicitud.strftime("%d-%m-%Y") if cotizacion.fechaSolicitud else "",
        "fechaCaducidad": cotizacion.fechaCaducidad.strftime("%d-%m-%Y") if cotizacion.fechaCaducidad else "",
        "tipoMoneda": {
            "id": cotizacion.tipoMoneda.id,
            "codigo": cotizacion.tipoMoneda.codigo,
            "descripcion": cotizacion.tipoMoneda.descripcion,
        },
        "iva": {
            "id": cotizacion.iva.id,
            "porcentaje": str(ivaPorcentaje)
        },
        "infoSistema": {
            "id": organizacion.infoSistema.id,
            "tipoMoneda": organizacion.infoSistema.tipoMoneda.id,
            "tipoCambioDolar": str(organizacion.infoSistema.tipoCambioDolar),
        },
        "descuento": str(descuentoPorcentaje),
        "cotizacionServicio": [
            {
                "id": cs.id,
                "descripcion": cs.descripcion,
                "precio": str(round(cs.precio, 2)),
                "cantidad": cs.cantidad,
                "cotizacion": cs.cotizacion.id,
                "servicio": cs.servicio.id,
                "servicioNombre": cs.servicio.nombreServicio,
                "subtotal": round(cs.precio * cs.cantidad, 2),
            } for cs in cotizacionServicios
        ],
        "valores": {
            "subtotal": str(subtotal),
            "descuento": str(descuentoPorcentaje),
            "valorDescuento": str(valorDescuento),
            "subtotalDescuento": str(subtotalDescuento),
            "iva": str(ivaPorcentaje),
            "ivaValor": str(ivaValor),
            "importe": str(importe)
        }
    }

    return JsonResponse(data, safe=False)

def contar_cotizaciones(request):
    #permission_classes = [IsAuthenticated]
    total_cotizaciones = Cotizacion.objects.count()
    
    # Contar las cotizaciones con estado ID = 3 (aceptadas)
    cotizaciones_aceptadas = Cotizacion.objects.filter(estado_id=3).count()
    
    # Calcular las cotizaciones no aceptadas
    cotizaciones_noaceptadas = total_cotizaciones - cotizaciones_aceptadas
    
    # Evitar división por cero
    porcentaje_aceptadas = (cotizaciones_aceptadas / total_cotizaciones) * 100 if total_cotizaciones > 0 else 0

    # Responder con un JSON
    data = {
        "cotizacionestotales": total_cotizaciones,
        "cotizacionesnoaceptadas": cotizaciones_noaceptadas,
        "cotizacionesaceptadas": cotizaciones_aceptadas,
        "porcentajeaceptadas": round(porcentaje_aceptadas, 2)  # Redondeamos a 2 decimales
    }

    return JsonResponse(data)

def crearOrdenTrabajo(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    cliente = cotizacion.cliente
    empresa = cliente.empresa

    direccionCliente = {
        "calle": cliente.calleCliente,
        "numero": cliente.numeroCliente,
        "colonia": cliente.coloniaCliente,
        "ciudad": cliente.ciudadCliente,
        "estado": cliente.estadoCliente,
        "codigoPostal": cliente.codigoPostalCliente
    }

    direccionEmpresa = {
        "calle": empresa.calle,
        "numero": empresa.numero,
        "colonia": empresa.colonia,
        "ciudad": empresa.ciudad,
        "estado": empresa.estado,
        "codigoPostal": empresa.codigoPostal
    }

    cotizacionServicios = CotizacionServicio.objects.filter(cotizacion=cotizacion)

    data = {
        "idCotizacion": cotizacion.id,
        "numero": cotizacion.numero,
        "cliente": {
            "nombreCompleto": f"{cliente.nombrePila} {cliente.apPaterno} {cliente.apMaterno}",
            "correo": cliente.correo,
            "direccion": direccionCliente
        },
        "empresa": {
            "nombre": empresa.nombre,
            "direccion": direccionEmpresa
        },
        "servicios": [
            {
                "id": cs.id,
                "descripcion": cs.descripcion,
                "cantidad": cs.cantidad,
                "servicio": {
                    "id": cs.servicio.id,
                    "nombre": cs.servicio.nombreServicio
                }
            } for cs in cotizacionServicios
        ]
    }

    return JsonResponse(data, safe=False)

def crearFactura(request, cotizacion_id):
    # Traemos la cotización con sus relaciones (incluye infoSistema para el tipo de cambio)
    cotizacion = get_object_or_404(
        Cotizacion.objects.select_related('cliente__empresa__organizacion__infoSistema'),
        id=cotizacion_id
    )
    cliente      = cotizacion.cliente
    empresa      = cliente.empresa
    organizacion = empresa.organizacion

    # — Emisor —
    cert = CertificadoSelloDigital.objects.filter(Organizacion=organizacion).first()
    rfc_emisor = cert.rfc if cert else ''
    emisor = {
        "nombre": organizacion.nombre,
        "rfc":    rfc_emisor,
        "direccion": {
            "calle":        organizacion.calle,
            "numero":       organizacion.numero,
            "colonia":      organizacion.colonia,
            "ciudad":       organizacion.ciudad,
            "estado":       organizacion.estado,
            "codigoPostal": organizacion.codigoPostal,
        }
    }

    # — Receptor —
    receptor = {
        "nombre": empresa.nombre,
        "rfc":    getattr(empresa, 'rfc', ''),
        "direccion": {
            "calle":        empresa.calle,
            "numero":       empresa.numero,
            "colonia":      empresa.colonia,
            "ciudad":       empresa.ciudad,
            "estado":       empresa.estado,
            "codigoPostal": empresa.codigoPostal,
        }
    }
    
    tipoMoneda={
        "id": cotizacion.tipoMoneda.id,
        "codigo": cotizacion.tipoMoneda.codigo,
        "descripcion": cotizacion.tipoMoneda.descripcion,
    }

    # — Servicios y cálculos —
    cs_qs = CotizacionServicio.objects.filter(cotizacion=cotizacion)

    # Subtotal bruto
    subtotal = sum(cs.precio * cs.cantidad for cs in cs_qs)

    # Descuento
    descuento_pct   = Decimal(cotizacion.descuento)
    valor_desc      = subtotal * descuento_pct / Decimal(100)
    subtotal_desc   = subtotal - valor_desc

    # IVA
    iva_pct   = Decimal(cotizacion.iva.porcentaje)
    iva_val    = subtotal_desc * iva_pct

    # Total antes de cambio
    importe = subtotal_desc + iva_val

    # ¿Convertir a USD?
    convertir = (cotizacion.tipoMoneda.id == 2)
    if convertir:
        tc = organizacion.infoSistema.tipoCambioDolar
        subtotal      /= tc
        valor_desc    /= tc
        subtotal_desc /= tc
        iva_val       /= tc
        importe       /= tc

    # Redondeo
    subtotal      = subtotal.quantize(Decimal('0.01'))
    valor_desc    = valor_desc.quantize(Decimal('0.01'))
    subtotal_desc = subtotal_desc.quantize(Decimal('0.01'))
    iva_val       = iva_val.quantize(Decimal('0.01'))
    importe       = importe.quantize(Decimal('0.01'))

    # Lista de servicios con precio y subtotal convertidos
    servicios = []
    for cs in cs_qs:
        precio_u = cs.precio
        linea_sub = cs.precio * cs.cantidad
        if convertir:
            precio_u   = precio_u / tc
            linea_sub  = linea_sub / tc

        servicios.append({
            "id":          cs.id,
            "metodo": {
                "id":     cs.servicio.metodos.id,
                "codigo": cs.servicio.metodos.codigo,
            },
            "descripcion": cs.descripcion,
            "cantidad":    cs.cantidad,
            "precio":      str(Decimal(precio_u).quantize(Decimal('0.01'))),
            "subtotal":    str(Decimal(linea_sub).quantize(Decimal('0.01'))),
            "servicio": {
                "id":     cs.servicio.id,
                "nombre": cs.servicio.nombreServicio,
            }
        })

    # Montaje del JSON de salida
    data = {
        "idCotizacion": cotizacion.id,
        "numero":       cotizacion.numero,
        "emisor":       emisor,
        "receptor":     receptor,
        "tipoMoneda":   tipoMoneda,
        "servicios":    servicios,
        "valores": {
            "subtotal":             str(subtotal),
            "descuentoPorcentaje":  str(descuento_pct),
            "valorDescuento":       str(valor_desc),
            "subtotalConDescuento": str(subtotal_desc),
            "ivaPorcentaje":        str(iva_pct),
            "ivaValor":             str(iva_val),
            "importe":              str(importe),
        }
    }

    return JsonResponse(data, safe=False)
