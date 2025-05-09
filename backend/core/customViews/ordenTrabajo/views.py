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

def dataOrdenTrabajoCrearFactura(request, orden_id):
    # Se obtiene la orden con relaciones
    orden = get_object_or_404(
        OrdenTrabajo.objects.select_related(
            'cotizacion__cliente__empresa__organizacion', 'estado'
        ),
        id=orden_id
    )

    empresa = orden.cotizacion.cliente.empresa
    organizacion = empresa.organizacion

    # Información del tipo de moneda de la cotización
    tipo_moneda = orden.cotizacion.tipoMoneda

    # Definir factor de conversión: en caso de que tipoMoneda sea 2,
    # se divide entre el atributo tipoCambioDolar del InfoSistema
    conversion_factor = Decimal("1")
    if tipo_moneda.id == 2:
        conversion_factor = organizacion.infoSistema.tipoCambioDolar

    servicios = OrdenTrabajoServicio.objects.filter(ordenTrabajo=orden)
    cotizacion_servicios = CotizacionServicio.objects.filter(cotizacion=orden.cotizacion)

    subtotal = Decimal("0")
    serviciosData = []

    for servicio_item in servicios:
        cs = None
        # Se busca el registro de CotizacionServicio que corresponda a este servicio,
        # utilizando además la descripción para diferenciar registros
        for cs_item in cotizacion_servicios:
            if (cs_item.servicio.id == servicio_item.servicio.id and
                cs_item.descripcion.strip() == servicio_item.descripcion.strip()):
                cs = cs_item
                break

        # Obtener el precio del servicio (si no se encuentra, 0)
        precio = cs.precio if cs else Decimal("0")
        # Aplicar el factor de conversión
        precio_convertido = precio / conversion_factor
        valor = precio * servicio_item.cantidad
        valor_convertido = valor / conversion_factor
        importe = precio_convertido * servicio_item.cantidad

        subtotal += valor_convertido

        serviciosData.append({
            "ordenTrabajoServicio": {
                "id": servicio_item.id,
                "cantidad": servicio_item.cantidad,
                "descripcion": servicio_item.descripcion
            },
            "cotizacionServicio": {
                "id": cs.id if cs else None,
                "precio": float(precio_convertido),
            },
            "servicio": {
                "id": servicio_item.servicio.id,
                "nombre": servicio_item.servicio.nombreServicio,
                "metodo": {
                    "id": servicio_item.servicio.metodos.id,
                    "codigo": servicio_item.servicio.metodos.codigo
                },
            },
            "importe": float(importe)
        })

    descuento_pct = orden.cotizacion.descuento
    factor_descuento = Decimal(descuento_pct) / Decimal(100)
    valorDescuento = subtotal * factor_descuento
    subtotalConDescuento = subtotal - valorDescuento

    iva_pct = orden.cotizacion.iva.porcentaje
    tasa_iva = Decimal(iva_pct)
    valor_iva = subtotalConDescuento * tasa_iva
    total = subtotalConDescuento + valor_iva

    data = {
        "ordenTrabajo": {
            "id": orden.id,
            "codigo": orden.codigo
        },
        "empresa": {
            "id": empresa.id,
            "nombre": empresa.nombre,
            "rfc": empresa.rfc,
            "direccion": {
                "calle": empresa.calle,
                "numero": empresa.numero,
                "colonia": empresa.colonia,
                "ciudad": empresa.ciudad,
                "estado": empresa.estado,
                "codigoPostal": empresa.codigoPostal,
            }
        },
        "organizacion": {
            "id": organizacion.id,
            "nombre": organizacion.nombre,
            "telefono": organizacion.telefono,
            "pagina": organizacion.pagina,
            "slogan": organizacion.slogan,
            "direccion": {
                "calle": organizacion.calle,
                "numero": organizacion.numero,
                "colonia": organizacion.colonia,
                "ciudad": organizacion.ciudad,
                "estado": organizacion.estado,
                "codigoPostal": organizacion.codigoPostal,
            }
        },
        "estado": {
            "id": orden.estado.id,
            "nombre": orden.estado.nombre,
        },
        "cotizacion": {
            "id": orden.cotizacion.id,
            "descuento": f"{descuento_pct}%",
            "iva": {
                "porcentaje": f"{iva_pct}%"
            },
            "tipoMoneda": {
                "id": tipo_moneda.id,
                "codigo": tipo_moneda.codigo,
                "descripcion": tipo_moneda.descripcion,
            }
        },
        "servicios": serviciosData,
        "valores": {
            "subtotal": float(subtotal),
            "descuento": f"{descuento_pct}%",
            "valorDescuento": float(valorDescuento),
            "subtotalDescuento": float(subtotalConDescuento),
            "tasaIVA": f"{tasa_iva:.2f}",
            "iva": float(valor_iva),
            "total": float(total)
        }
    }

    return JsonResponse(data, safe=False)

def allOrdenTrabajoData(request, organizacion_id):
    #permission_classes = [IsAuthenticated]
    ordenes = OrdenTrabajo.objects.select_related(
        'cotizacion__cliente__empresa', 
        'estado',
        'receptor'
    ).filter(cotizacion__cliente__empresa__organizacion_id=organizacion_id)

    data = []
    for orden in ordenes:
        # Nombre completo del contacto (cliente)
        nombreCompleto = f"{orden.cotizacion.cliente.nombrePila} {orden.cotizacion.cliente.apPaterno}"
        if orden.cotizacion.cliente.apMaterno:
            nombreCompleto += f" {orden.cotizacion.cliente.apMaterno}"

        # Nombre completo del receptor
        nombreReceptor = f"{orden.receptor.nombrePila} {orden.receptor.apPaterno}"
        if orden.receptor.apMaterno:
            nombreReceptor += f" {orden.receptor.apMaterno}"

        data.append({
            "orden": orden.id,
            "numero": orden.numero,
            "codigo": orden.codigo,
            "contacto": nombreCompleto,
            "receptor": nombreReceptor,
            "expiracion": orden.cotizacion.fechaCaducidad,
            "estado": {
                "id": orden.estado.id,
                "nombre": orden.estado.nombre,
            },
            "organizacion": orden.cotizacion.cliente.empresa.organizacion.id,
        })

    return JsonResponse(data, safe=False)

def dataOrdenTrabajo(request, orden_id):
    #permission_classes = [IsAuthenticated]
    orden = get_object_or_404(OrdenTrabajo.objects.select_related(
        'cotizacion__cliente__empresa', 'estado', 'receptor'
    ), id=orden_id)

    # Extraer la información del cliente
    cliente = orden.cotizacion.cliente
    empresa = cliente.empresa

    # Obtener los servicios asociados a la orden de trabajo
    servicios = OrdenTrabajoServicio.objects.filter(ordenTrabajo=orden)

    # Construir la lista de servicios
    serviciosData = [
        {
            "id": servicio.id,
            "cantidad": servicio.cantidad,
            "descripcion": servicio.descripcion,
            "servicio": {
                "id": servicio.servicio.id,
                "nombre": servicio.servicio.nombreServicio,
                "metodo": {
                    "id": servicio.servicio.metodos.id,
                    "codigo": servicio.servicio.metodos.codigo
                },
            }
        }
        for servicio in servicios
    ]

    # Construir el JSON de respuesta
    data = {
        "orden":{
            "id":orden.id,
            "numero":orden.numero,
            "codigo":orden.codigo,
        },
        "cliente": {
            "nombreCompleto": f"{cliente.nombrePila} {cliente.apPaterno} {cliente.apMaterno or ''}".strip(),
            "correo": cliente.correo,
            "telefono": cliente.telefono,
            "celular": cliente.celular,
            "direccion": {
                "calle": cliente.calleCliente,
                "numero": cliente.numeroCliente,
                "colonia": cliente.coloniaCliente,
                "ciudad": cliente.ciudadCliente,
                "estado": cliente.estadoCliente,
                "codigoPostal": cliente.codigoPostalCliente,
            }
        },
        "empresa": {
            "nombre": empresa.nombre,
            "rfc": empresa.rfc,
            "direccion": {
                "calle": empresa.calle,
                "numero": empresa.numero,
                "colonia": empresa.colonia,
                "ciudad": empresa.ciudad,
                "estado": empresa.estado,
                "codigoPostal": empresa.codigoPostal,
                "organizacion": empresa.organizacion.id,
            }
        },
        "receptor": {
            "nombreCompleto": f"{orden.receptor.nombrePila} {orden.receptor.apPaterno} {orden.receptor.apMaterno or ''}".strip(),
            "correo": orden.receptor.correo,
            "celular": orden.receptor.celular,
        },
        "estado": {
            "id": orden.estado.id,
            "nombre": orden.estado.nombre,
        },
        "cotizacion": {
            "id": orden.cotizacion.id,
        },
        "servicios": serviciosData  # Agregamos la lista de servicios
    }

    return JsonResponse(data, safe=False)

def dataEditOrdenTrabajo(request, orden_id):
    # Obtenemos la orden de trabajo con su receptor
    orden = get_object_or_404(OrdenTrabajo.objects.select_related('receptor'), id=orden_id)
    
    # Obtenemos los registros de OrdenTrabajoServicio asociados a la orden
    ots_list = OrdenTrabajoServicio.objects.filter(ordenTrabajo=orden)
    
    # Construir la lista de servicios asociados, incluyendo:
    # id de la OrdenTrabajoServicio, y dentro del objeto "servicio": id y nombre.
    # Además se incluyen los campos cantidad y descripcion que pertenecen a OrdenTrabajoServicio.
    serviciosData = [
        {
            "id": ots.id,
            "servicio": {
                "id": ots.servicio.id,
                "nombre": ots.servicio.nombreServicio,
            },
            "cantidad": ots.cantidad,
            "descripcion": ots.descripcion,
        }
        for ots in ots_list
    ]
    
    # Construir la respuesta JSON con la información requerida
    data = {
        "ordenTrabajo": {
            "id": orden.id,
            "codigo": orden.codigo,
        },
        "receptor": {
            "id": orden.receptor.id,
            "nombreCompleto": f"{orden.receptor.nombrePila} {orden.receptor.apPaterno} {orden.receptor.apMaterno or ''}".strip(),
        },
        "ordenTrabajoServicios": serviciosData
    }
    
    return JsonResponse(data, safe=False)
