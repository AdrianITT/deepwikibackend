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

def allClientesData(request, organizacion_id):
    """
    Devuelve todos los clientes pertenecientes a la organización indicada,
    incluyendo nombre completo, sus atributos clave y los datos relevantes de la empresa asociada.
    """
    clientes = Cliente.objects.select_related(
        'empresa__organizacion', 'empresa__UsoCfdi', 'empresa__regimenFiscal', 'titulo'
    ).filter(empresa__organizacion_id=organizacion_id)

    data = []
    for c in clientes:
        empresa = c.empresa
        direccion_empresa = f"{empresa.calle} {empresa.numeroExterior or ''}, {empresa.colonia}, {empresa.codigoPostal}, {empresa.ciudad}, {empresa.estado}"

        nombre_completo = f"{c.nombrePila} {c.apPaterno}"
        if c.apMaterno:
            nombre_completo += f" {c.apMaterno}"

        data.append({
            "id": c.id,
            "numero": c.numero,
            "nombrePila": c.nombrePila,
            "apPaterno": c.apPaterno,
            "apMaterno": c.apMaterno,
            "nombreCompleto": nombre_completo.strip(),
            "correo": c.correo,
            "division": c.division,
            "codigopostalcliente": c.codigoPostalCliente,
            "empresa": {
                "id": empresa.id,
                "numero": empresa.numero,
                "nombre": empresa.nombre,
                "rfc": empresa.rfc,
                "codigoPostal": empresa.codigoPostal,
                "ciudad": empresa.ciudad,
                "estado": empresa.estado,
                "colonia": empresa.colonia,
                "numeroExterior": empresa.numeroExterior,
                "calle": empresa.calle,
                "organizacion": empresa.organizacion.nombre,
                "direccioncompleta": direccion_empresa.strip(),
            }
        })

    return JsonResponse(data, safe=False)

def direccionclienteempresa(request, cliente_id):
    #permission_classes = [IsAuthenticated]
    cliente = get_object_or_404(Cliente, id=cliente_id)
    empresa = cliente.empresa

    data = {
        "cliente": {
            "id": cliente.id,
            "empresa": {
                "id": empresa.id,
                "nombre": empresa.nombre,
                "calle": empresa.calle,
                "numero": empresa.numero,
                "colonia": empresa.colonia,
                "ciudad": empresa.ciudad,
                "estado": empresa.estado,
                "codigoPostal": empresa.codigoPostal,
            },
        }
    }

    return JsonResponse(data, safe=False)

def clienteFactura(request, cliente_id):
    """
    Retorna todas las facturas asociadas a un cliente,
    navegando Factura -> Cotizacion -> Cliente.
    """
    # 1) Traemos facturas con cotización → cliente → moneda de la cotización
    facturas = (
        Factura.objects
        .select_related('cotizacion__cliente', 'cotizacion__tipoMoneda')
        .filter(cotizacion__cliente__id=cliente_id)
    )

    if not facturas.exists():
        return JsonResponse(
            {"error": "No se encontraron facturas para este cliente"},
            status=404
        )

    data = []
    for factura in facturas:
        cot = factura.cotizacion
        cli = cot.cliente
        moneda = cot.tipoMoneda

        # Nombre completo del cliente
        nombre_completo = f"{cli.nombrePila} {cli.apPaterno}"
        if cli.apMaterno:
            nombre_completo += f" {cli.apMaterno}"

        # Importe con dos decimales si existe
        importe = None
        if factura.importe is not None:
            importe = str(Decimal(factura.importe).quantize(Decimal('0.01')))

        data.append({
            "factura_id":      factura.id,
            "facturanumero":    factura.numero,
            "notas":           factura.notas,
            "ordenCompra":     factura.ordenCompra,
            "fechaExpedicion": factura.fechaExpedicion,
            "importe":         importe,
            "tipoMoneda": {
                "id":          moneda.id,
                "codigo":      moneda.codigo,
                "descripcion": moneda.descripcion,
            },
            # Datos del cliente receptor
            "cliente": {
                "cliente_id":     cli.id,
                "nombreCompleto": nombre_completo,
                "correo":         cli.correo,
                "telefono":       getattr(cli, 'telefono', ''),
                "celular":        getattr(cli, 'celular', ''),
            },
            # Datos de la cotización asociada
            "cotizacion": {
                "cotizacion_id": cot.id,
                "numero":        cot.numero,
                "denominacion":  cot.denominacion,
            }
        })

    return JsonResponse(data, safe=False)

def editcliente(request, cliente_id):
    try:
        cliente = Cliente.objects.select_related('empresa').get(id=cliente_id)
        empresa = cliente.empresa

        data = {
            'cliente': {
                'id': cliente.id,
                'nombrePila': cliente.nombrePila,
                'apPaterno': cliente.apPaterno,
                'apMaterno': cliente.apMaterno,
                'correo': cliente.correo,
                'telefono': cliente.telefono,
                'celular': cliente.celular,
                'fax': cliente.fax,
                'codigoPostalCliente': cliente.codigoPostalCliente,
                'ciudadCliente': cliente.ciudadCliente,
                'estadoCliente': cliente.estadoCliente,
                'coloniaCliente': cliente.coloniaCliente,
                'numeroCliente': cliente.numeroCliente,
                'calleCliente': cliente.calleCliente,
                'division': cliente.division,
                'titulo_id': cliente.titulo_id,
            },
            'empresa': {
                'id': empresa.id,
                'direccion': {
                    'codigoPostal': empresa.codigoPostal,
                    'ciudad': empresa.ciudad,
                    'estado': empresa.estado,
                    'colonia': empresa.colonia,
                    'numero': empresa.numero,
                    'calle': empresa.calle,
                }
            }
        }
        return JsonResponse(data)

    except Cliente.DoesNotExist:
        raise Http404("Cliente no encontrado")

"ESTA VISTA SE PROBARA HASTA QUE SE PUEDA MANDAR ALGUNA DE LAS NUEVAS FACTURAS A FACTURAMA"
def clienteConFactura(request, organizacion_id):
    """
    Retorna una lista de clientes que cumplen:
      - Pertenecen a la organización indicada.
      - Tienen al menos una cotización.
      - Esa cotización tiene al menos una factura (directa sobre cotización).
      - Dicha factura cuenta con al menos un registro en FacturaFacturama.
    """
    clientes = (
        Cliente.objects
        # Navegamos Cliente → Cotizacion → Factura → FacturaFacturama
        .filter(
            cotizacion__factura__facturafacturama__isnull=False,
            empresa__organizacion_id=organizacion_id,
        )
        .distinct()
        .select_related('empresa')  # para acceder rápido a empresa.organizacion si se necesitara
    )

    data = []
    for cliente in clientes:
        nombre_completo = f"{cliente.nombrePila} {cliente.apPaterno}"
        if cliente.apMaterno:
            nombre_completo += f" {cliente.apMaterno}"

        data.append({
            "cliente_id":     cliente.id,
            "nombreCompleto": nombre_completo,
        })

    return JsonResponse(data, safe=False)

def listaClientes(request, organizacion_id):
    clientes = Cliente.objects.select_related('empresa').filter(empresa__organizacion_id=organizacion_id)

    data = []
    for cliente in clientes:
        nombreCompleto = f"{cliente.nombrePila} {cliente.apPaterno} {cliente.apMaterno or ''}".strip()
        data.append({
            'id': cliente.id,
            'nombreCompleto': nombreCompleto,
            'empresa': {
                'id': cliente.empresa.id,
                'nombre': cliente.empresa.nombre
            }
        })

    return JsonResponse(data, safe=False)