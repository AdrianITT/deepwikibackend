from django.shortcuts import render, get_object_or_404
from backend.settings import EMAIL_HOST_USER,PASSWORD,SANDBOX_URL,USERNAME
import requests
from django.http import JsonResponse, HttpResponse
from django.db import connection
from datetime import datetime, timedelta
import pytz
from datetime import datetime, timezone, time
import os, base64, json
from django.conf import settings
from .models import RegimenFiscal, TipoMoneda, Iva, ImagenMarcaAgua, Rol 
from .models import Titulo, UnidadCfdi, Metodos, ClaveCfdi, ObjetoImpuesto
from .models import Estado, Receptor, InfoOrdenTrabajo, InfoCotizacion
from .models import InfoSistema, Organizacion, Empresa, Cliente, Servicio
from .models import Cotizacion, OrdenTrabajo, Factura
from .models import CertificadoSelloDigital, User, OrdenTrabajoServicio
from .models import FacturaFacturama, CotizacionServicio, ComprobantePagoFactura
from .models import TipoCfdi, FormaPago, MetodoPago, UsoCfdi, FacturaServicio
from .models import PreCotizacion, PreCotizacionServicio, ComprobantePago
from .serializers import RegimenFiscalSerializer, TipoMonedaSerializer, IvaSerializer, ImagenMarcaAguaSerializer, RolSerializer
from .serializers import TituloSerializer, UnidadCfdiSerializer, MetodosSerializer, ClaveCfdiSerializer, ObjetoImpuestoSerializer
from .serializers import EstadoSerializer, ReceptorSerializer, InfoOrdenTrabajoSerializer, InfoCotizacionSerializer
from .serializers import InfoSistemaSerializer, OrganizacionSerializer, EmpresaSerializer, ClienteSerializer, ServicioSerializer
from .serializers import CotizacionSerializer, OrdenTrabajoSerializer, FacturaSerializer, ComprobantePagoFacturaSerializer
from .serializers import CertificadoSelloDigitalSerializer, FacturaFacturamaSerializer, ComprobantePagoSerializer
from .serializers import CotizacionServicioSerializer, UserSerializer, OrdenTrabajoServicioSerializer, FacturaServicioSerializer
from .serializers import TipoCfdiSerializer, FormaPagoSerializer, MetodoPagoSerializer, UsoCfdiSerializer
from .serializers import PreCotizacionSerializer, PreCotizacionServicioSerializer
from rest_framework import viewsets, status, permissions, generics, filters
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.template.loader import render_to_string
from weasyprint import HTML
from decimal import Decimal, ROUND_HALF_UP
import io
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from django.http import JsonResponse
from django.db import connection
from decimal import Decimal, ROUND_HALF_UP
from django.utils.timezone import now  # Importar la función now() para obtener la fecha actual
from collections import defaultdict


class RegimenFiscalViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = RegimenFiscal.objects.all()
    serializer_class = RegimenFiscalSerializer

class TipoMonedaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = TipoMoneda.objects.all()
    serializer_class = TipoMonedaSerializer

class IvaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Iva.objects.all()
    serializer_class = IvaSerializer

class ImagenMarcaAguaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = ImagenMarcaAgua.objects.all()
    serializer_class = ImagenMarcaAguaSerializer

class RolViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TituloViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Titulo.objects.all()
    serializer_class = TituloSerializer

class UnidadCfdiViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = UnidadCfdi.objects.all()
    serializer_class = UnidadCfdiSerializer

class MetodosViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Metodos.objects.all()
    serializer_class = MetodosSerializer

class ClaveCfdiViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = ClaveCfdi.objects.all()
    serializer_class = ClaveCfdiSerializer

class ObjetoImpuestoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = ObjetoImpuesto.objects.all()
    serializer_class = ObjetoImpuestoSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class TipoCfdiViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = TipoCfdi.objects.all()
    serializer_class = TipoCfdiSerializer

class FormaPagoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoSerializer
    
class MetodoPagoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    
class UsoCfdiViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = UsoCfdi.objects.all()
    serializer_class = UsoCfdiSerializer

class ReceptorViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Receptor.objects.all()
    serializer_class = ReceptorSerializer

class InfoOrdenTrabajoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = InfoOrdenTrabajo.objects.all()
    serializer_class = InfoOrdenTrabajoSerializer

class InfoCotizacionViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = InfoCotizacion.objects.all()
    serializer_class = InfoCotizacionSerializer

class InfoSistemaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = InfoSistema.objects.all()
    serializer_class = InfoSistemaSerializer

class OrganizacionViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Organizacion.objects.all()
    serializer_class = OrganizacionSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class CotizacionViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer

class CotizacionServicioViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = CotizacionServicio.objects.all()
    serializer_class = CotizacionServicioSerializer
    
class PreCotizacionViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = PreCotizacion.objects.all()
    serializer_class = PreCotizacionSerializer
    
class PreCotizacionServicioViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = PreCotizacionServicio.objects.all()
    serializer_class = PreCotizacionServicioSerializer
    
class OrdenTrabajoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer
    
class OrdenTrabajoServicioViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = OrdenTrabajoServicio.objects.all()
    serializer_class = OrdenTrabajoServicioSerializer

class FacturaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    
class FacturaServicioViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = FacturaServicio.objects.all()
    serializer_class = FacturaServicioSerializer
    
class CertificadoSelloDigitalViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated] 
    queryset = CertificadoSelloDigital.objects.all()
    serializer_class = CertificadoSelloDigitalSerializer

class FacturaFacturamaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = FacturaFacturama.objects.all()
    serializer_class = FacturaFacturamaSerializer
    
class ComprobantePagoViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = ComprobantePago.objects.all()
    serializer_class = ComprobantePagoSerializer
    
class ComprobantePagoFacturaViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = ComprobantePagoFactura.objects.all()
    serializer_class = ComprobantePagoFacturaSerializer
    
def pagosFactura(request, factura_id):
    #permission_classes = [IsAuthenticated]
    factura = get_object_or_404(Factura, pk=factura_id)
    
    pagos_facturas = ComprobantePagoFactura.objects.filter(factura=factura)
    
    datos_pagos = []
    for pf in pagos_facturas:
        pago = pf.comprobantepago
        datos_pagos.append({
            'id': pago.id,
            'facturama_id': pago.facturama_id,
            'observaciones': pago.observaciones,
            'fechaPago': pago.fechaPago,
            'formaPago_id': pago.formapago.id if pago.formapago else None,
            'montototal': pf.montototal,
            'montopago': pf.montopago,
            'montorestante': pf.montorestante,
            'parcialidad': pf.parcialidad,
        })
    
    return JsonResponse({'pagos': datos_pagos})

def cfdis_all(emisor_rfc):
    #permission_classes = [IsAuthenticated]
    url = f"{SANDBOX_URL}/api-lite/cfdis?status=all&issued={emisor_rfc}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    return None

def crear_cfdi_api(data):
    #permission_classes = [IsAuthenticated]
    url = f"{SANDBOX_URL}/api-lite/3/cfdis"
    response = requests.post(url, json=data, auth=(USERNAME, PASSWORD))
    return response.json()  # Puedes devolver la respuesta en formato JSON

def get_cfdi_doc(doc, id_factura):
    #permission_classes = [IsAuthenticated]
    url = f"{SANDBOX_URL}/cfdi/{doc}/issuedLite/{id_factura}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    return response.json()

def cancelar_factura_api(idfactura, uuid):
    """
    Cancela una factura utilizando la API de Facturama.
    Siempre devuelve una tupla (success: bool, response: dict|str).
    """
    url = f"{SANDBOX_URL}/api-lite/cfdis/{idfactura}"
    try:
        # Enviamos el uuid como parámetro de consulta
        resp = requests.delete(url, params={"uuid": uuid}, auth=(USERNAME, PASSWORD))
        # Si la API responde 200 OK
        if resp.status_code == 200:
            try:
                return True, resp.json()
            except ValueError:
                # JSON mal formado o vacío
                return True, "Respuesta vacía o no JSON válido"
        # Cualquier otro status code lo tratamos como error
        else:
            try:
                return False, resp.json()
            except ValueError:
                return False, resp.text
    except requests.exceptions.RequestException as e:
        # Errores de conexión, timeouts, etc.
        return False, str(e)

def get_factura_data(request, factura_id):
    # 1) Traer la factura y sus relaciones
    factura = get_object_or_404(
        Factura.objects.select_related(
            'cotizacion__cliente__empresa__organizacion__RegimenFiscal',
            'cotizacion__cliente__empresa__regimenFiscal',
            'cotizacion__cliente__empresa__organizacion__infoSistema',
            'tipoCfdi',
            'formaPago',
            'metodoPago',
            'cotizacion__iva',
            'cotizacion__tipoMoneda',
        ),
        pk=factura_id
    )

    cotizacion   = factura.cotizacion
    cliente      = cotizacion.cliente
    empresa      = cliente.empresa
    organizacion = empresa.organizacion

    # RFC del emisor
    cert = CertificadoSelloDigital.objects.filter(Organizacion=organizacion).first()
    organizacion_rfc = cert.rfc if cert else ''

    # Tipo de cambio
    if cotizacion.tipoMoneda.id == 2:
        tipo_cambio = organizacion.infoSistema.tipoCambioDolar
    else:
        tipo_cambio = Decimal('1')

    # Fechas y datos básicos
    fecha_iso = factura.fechaExpedicion.isoformat()
    regimen_fiscal = organizacion.RegimenFiscal
    

    facturamulti = {
        "NameId": "1",
        "LogoUrl": f"https://simplaxi.com/media{organizacion.logo.url if organizacion.logo else ''}",        
        "Date": fecha_iso,
        "Serie": "FAC",
        "CurrencyExchangeRate": float(tipo_cambio) if tipo_cambio != 1 else None,
        "Currency": cotizacion.tipoMoneda.codigo,
        "ExpeditionPlace": organizacion.codigoPostal,
        "Folio": factura.id,
        "CfdiType":      factura.tipoCfdi.codigo,
        "PaymentForm":   factura.formaPago.codigo,
        "PaymentMethod": factura.metodoPago.codigo,
        "Issuer": {
            "FiscalRegime": regimen_fiscal.codigo,
            "Rfc":          organizacion_rfc,
            "Name":         organizacion.nombre,
        },
        "Receiver": {
            "Rfc":           empresa.rfc,
            "CfdiUse":       getattr(empresa, 'UsoCfdi').codigo if hasattr(empresa, 'UsoCfdi') and empresa.UsoCfdi else '',
            "Name":          empresa.nombre,
            "FiscalRegime":  empresa.regimenFiscal.codigo if empresa.regimenFiscal else '',
            "TaxZipCode":    empresa.codigoPostal,
        },
        "Items":        [],
        "Observations": factura.notas,
        "OrderNumber":  factura.ordenCompra,
    }

    # 4) Factor de descuento de factura
    pct_factura   = Decimal(factura.porcentaje or 0)
    factor_factura = (Decimal(100) - pct_factura) / Decimal(100)

    # 5) Cargar servicios de la factura
    fs_qs = FacturaServicio.objects.select_related(
        'servicio__claveCfdi',
        'servicio__unidadCfdi',
        'servicio__metodos'
    ).filter(factura=factura)

    rounding = Decimal('0.01')

    for fs in fs_qs:
        servicio = fs.servicio
        cantidad = Decimal(fs.cantidad)

        # 5.1) Precio unitario ya convertidos, solo aplicamos descuento de factura
        precio_desc = (Decimal(fs.precio) * factor_factura).quantize(rounding, ROUND_HALF_UP)

        # 5.2) Subtotal por línea
        subtotal_linea = (precio_desc * cantidad).quantize(rounding, ROUND_HALF_UP)

        # 5.3) Descuento de cotización
        pct_cot    = Decimal(cotizacion.descuento or 0) / Decimal(100)
        valor_desc = (subtotal_linea * pct_cot).quantize(rounding, ROUND_HALF_UP)
        subc_desc  = (subtotal_linea - valor_desc).quantize(rounding, ROUND_HALF_UP)

        # 5.4) IVA de cotización (tasa en fracción)
        pct_iva = (Decimal(cotizacion.iva.porcentaje or 0) / Decimal(1)).quantize(rounding, ROUND_HALF_UP)
        iva_val = (subc_desc * pct_iva).quantize(rounding, ROUND_HALF_UP)

        # 5.5) Total de línea
        total_linea = (subc_desc + iva_val).quantize(rounding, ROUND_HALF_UP)

        # 5.6) Armar ítem
        facturamulti["Items"].append({
            "IdProduct":   None,
            "ProductCode": servicio.claveCfdi.codigo,
            "Description": fs.servicio.nombreServicio,
            "Unit":        "Servicio",
            "UnitCode":    servicio.unidadCfdi.codigo,
            "UnitPrice":   float(precio_desc),
            "Quantity":    float(cantidad),
            "Subtotal":    float(subtotal_linea),
            "Discount":    float(valor_desc),
            "TaxObject":   "02",
            "Taxes": [
                {
                    "Total":       float(iva_val),
                    "Name":        "IVA",
                    "Base":        float(subc_desc),
                    "Rate":        float(pct_iva),
                    "IsRetention": False
                }
            ],
            "Total": float(total_linea),
        })

    # 6) Llamada a Facturama y guardado
    response = crear_cfdi_api(facturamulti)
    comp = response.get("Complement", {})
    if response.get("Id") and comp.get("TaxStamp", {}).get("Uuid"):
        FacturaFacturama.objects.create(
            uuid=comp["TaxStamp"]["Uuid"],
            idfactura=response["Id"],
            factura_id=factura.id
        )
        return JsonResponse({"success": True, "cfdi": response})
    return JsonResponse({"error": "Error creando CFDI", "response": response}, status=400)
    
def factura_detail(request, factura_id):
    #permission_classes = [IsAuthenticated]
    """
    Vista para obtener los detalles de una factura específica.
    """
    try:
        # Verificar que el factura_id existe en FacturaFacturama
        try:
            factura_facturama = FacturaFacturama.objects.get(factura_id=factura_id)
        except FacturaFacturama.DoesNotExist:
            return JsonResponse({"error": "El factura_id proporcionado no existe en FacturaFacturama."}, status=404)

        # Utilizar el idfactura de FacturaFacturama para realizar la consulta
        idfactura = factura_facturama.idfactura

        # Construir la URL para la API de Facturama
        url = f"{SANDBOX_URL}/api-lite/cfdis/{idfactura}"
        response = requests.get(url, auth=(USERNAME, PASSWORD))

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            factura_data = response.json()
            return JsonResponse(factura_data, safe=False)
        elif response.status_code == 404:
            return JsonResponse({"error": "Factura no encontrada en la API de Facturama."}, status=404)
        else:
            return JsonResponse({"error": "Error al consultar la factura en la API de Facturama."}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

def factura_delete(request, factura_id):
    """
    Vista para eliminar una factura específica utilizando el factura_id.
    """
    try:
        factura_facturama = FacturaFacturama.objects.get(factura_id=factura_id)
    except FacturaFacturama.DoesNotExist:
        return JsonResponse(
            {"error": "El factura_id proporcionado no existe en FacturaFacturama."},
            status=404
        )

    # Guardamos la instancia de Factura antes de eliminar la relación
    factura_obj = factura_facturama.factura
    idfactura = factura_facturama.idfactura
    uuid = factura_facturama.uuid

    # Primero cancelamos en Facturama
    success, api_response = cancelar_factura_api(idfactura, uuid)
    if not success:
        return JsonResponse(
            {"error": "Error al cancelar la factura en Facturama.", "response": api_response},
            status=400
        )

    # Si la cancelación fue exitosa, eliminamos localmente
    factura_facturama.delete()  # elimina el registro en FacturaFacturama
    factura_obj.delete()         # elimina el registro en Factura

    return JsonResponse({
        "success": "Factura cancelada y eliminada exitosamente.",
        "response": api_response
    })

def factura_pdf(request, factura_id):
    #permission_classes = [IsAuthenticated]
    try:
        # Buscar el registro en FacturaFacturama para obtener el idfactura
        try:
            factura_facturama = FacturaFacturama.objects.get(factura_id=factura_id)
        except FacturaFacturama.DoesNotExist:
            return JsonResponse({"error": "El factura_id proporcionado no existe en FacturaFacturama."}, status=404)
        
        id_factura = factura_facturama.idfactura

        # URL para obtener el PDF de Facturama
        url = f"{SANDBOX_URL}/cfdi/pdf/issuedLite/{id_factura}"
        response = requests.get(url, auth=(USERNAME, PASSWORD))

        if response.status_code == 200:
            pdf_data = response.json()

            # Verificar si el contenido está codificado en Base64
            if "Content" in pdf_data and "ContentType" in pdf_data and pdf_data["ContentType"] == "pdf":
                pdf_content = base64.b64decode(pdf_data["Content"])

                # Crear la respuesta de archivo PDF
                response = HttpResponse(pdf_content, content_type="application/pdf")
                response["Content-Disposition"] = f"attachment; filename=factura_{factura_id}.pdf"
                return response
            else:
                return JsonResponse({"error": "El contenido del PDF no está disponible o es inválido."}, status=400)
        else:
            return JsonResponse({"error": f"Error al obtener el PDF de Facturama: {response.text}"}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": f"Error al procesar la solicitud: {str(e)}"}, status=500)

def factura_xml(request, factura_id):
    #permission_classes = [IsAuthenticated]
    try:
        # Buscar el registro en FacturaFacturama para obtener el idfactura
        try:
            factura_facturama = FacturaFacturama.objects.get(factura_id=factura_id)
        except FacturaFacturama.DoesNotExist:
            return JsonResponse({"error": "El factura_id proporcionado no existe en FacturaFacturama."}, status=404)
        
        id_factura = factura_facturama.idfactura

        # URL para obtener el XML de Facturama
        url = f"{SANDBOX_URL}/cfdi/xml/issuedLite/{id_factura}"
        response = requests.get(url, auth=(USERNAME, PASSWORD))

        if response.status_code == 200:
            xml_data = response.json()

            # Verificar si el contenido está codificado en Base64
            if "Content" in xml_data and "ContentType" in xml_data and xml_data["ContentType"] == "xml":
                xml_content = base64.b64decode(xml_data["Content"])

                # Crear la respuesta de archivo XML
                response = HttpResponse(xml_content, content_type="application/xml")
                response["Content-Disposition"] = f"attachment; filename=factura_{factura_id}.xml"
                return response
            else:
                return JsonResponse({"error": "El contenido del XML no está disponible o es inválido."}, status=400)
        else:
            return JsonResponse({"error": f"Error al obtener el XML de Facturama: {response.text}"}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": f"Error al procesar la solicitud: {str(e)}"}, status=500)
    
def carga_csd(request, organizacion_id):
    #permission_classes = [IsAuthenticated]
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT rfc, archivocer, archivokey, contrasenia 
            FROM core_certificadosellodigital 
            WHERE Organizacion_id = %s
            
        """, [organizacion_id])

        rows = cursor.fetchall()

        if rows:
            rfc = rows[0][0]
            certificate_path = os.path.join(settings.MEDIA_ROOT, rows[0][1])  # Ruta completa
            private_key_path = os.path.join(settings.MEDIA_ROOT, rows[0][2])  # Ruta completa
            private_key_password = rows[0][3]  # Contraseña de la llave privada

            # Verificar que los archivos existen
            if not os.path.exists(certificate_path) or not os.path.exists(private_key_path):
                return JsonResponse({"error": "No se encontraron los archivos de certificado o llave."})

            try:
                # Leer el contenido de los archivos
                with open(certificate_path, 'rb') as cert_file:
                    certificate = cert_file.read()

                with open(private_key_path, 'rb') as key_file:
                    private_key = key_file.read()

                # Convertir a base64
                certificate_base64 = base64.b64encode(certificate).decode('utf-8')
                private_key_base64 = base64.b64encode(private_key).decode('utf-8')

                # Crear el payload
                payload = {
                    "Rfc": rfc,
                    "Certificate": certificate_base64,
                    "PrivateKey": private_key_base64,
                    "PrivateKeyPassword": private_key_password
                }

                # Enviar solicitud a Facturama
                api_url = f"{SANDBOX_URL}/api-lite/csds"
                response = requests.post(api_url, json=payload, auth=(USERNAME, PASSWORD))

                if response.status_code == 200:
                    return JsonResponse({"message": "CSD cargado exitosamente."})
                else:
                    print("Error detallado:", response.text)
                    return JsonResponse({"error": f"Error al cargar el CSD: {response.text}"})
            except Exception as e:
                return JsonResponse({"error": f"Error al procesar los archivos: {str(e)}"})
        else:
            return JsonResponse({"error": "No se encontraron CSDs para la organización."})
        
def borrar_csd(request, organizacion_id):
    #permission_classes = [IsAuthenticated]
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT rfc 
            FROM core_certificadosellodigital 
            WHERE Organizacion_id = %s
        """, [organizacion_id])
        rows = cursor.fetchall()

    if rows:
        rfc = rows[0][0]
        try:
            # Construir la URL para la eliminación en Facturama
            api_url = f"{SANDBOX_URL}/api-lite/csds/{rfc}"
            response = requests.delete(api_url, auth=(USERNAME, PASSWORD))

            if response.status_code == 200:
                # Eliminar el CSD de la base de datos
                with connection.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM core_certificadosellodigital 
                        WHERE Organizacion_id = %s
                    """, [organizacion_id])

                return JsonResponse({"message": "CSD borrado exitosamente de Facturama y la base de datos."})
            else:
                print("Error detallado:", response.text)
                return JsonResponse({"error": f"Error al borrar el CSD en Facturama: {response.text}"})
        except Exception as e:
            return JsonResponse({"error": f"Error al borrar el CSD: {str(e)}"})
    else:
        return JsonResponse({"error": "No se encontró CSD para la organización."})
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print("Solicitud de login recibida")
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        id = user.id
        rol = user.rol.name if user.rol else None
        organizacion = user.organizacion.nombre if user.organizacion else None
        organizacion_id = user.organizacion.id if user.organizacion else None

        # Asegúrate de que las cadenas estén codificadas en UTF-8
        print(f"Token generado: {token.key}".encode('utf-8'))
        print(f"Usuario: {user.username}, Id de Usuario: {id}, Rol: {rol}, Organización: {organizacion}, Organización ID: {organizacion_id}".encode('utf-8'))

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'rol': rol,
            'organizacion': organizacion,
            'organizacion_id': organizacion_id
        })
        
class LogoutView(APIView):
    #permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print("Solicitud de logout recibida")
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Token '):
                token_key = auth_header.split(' ')[1]
                token = Token.objects.get(key=token_key)
                print(f"Token a eliminar: {token.key}")
                token.delete()
                print("Token eliminado")
                return Response(status=status.HTTP_200_OK)
            else:
                print("No se encontró el token en la solicitud")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            print("Token no válido")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error al procesar la solicitud de logout: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generar_pdf_cotizacion(request, cotizacion_id):
    #permission_classes = [IsAuthenticated]
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return HttpResponse("Usuario no autenticado.", status=401)

    query = """
    SELECT
        org.logo as logo,
        org.nombre AS nombreOrganizacion,
        ic.nombreFormato AS nombreFormatoCotizacion,
        ic.version AS versionFormatoCotizacion,
        ic.fechaEmision AS fechaEmisionFormatoCotizacion,
        ic.tituloDocumento AS tituloDocumentoCotizacion,
        cli.titulo_id as clientetitulo,
        tit.abreviatura as tituloab,
        cli.nombrePila as clientenombre,
        cli.apPaterno as clienteappaterno,
        cli.apMaterno as clienterapmaterno,
        emp.nombre as empresanombre,
        cli.calleCliente as empresacalle,
        cli.numeroCliente as empresanumero,
        cli.coloniaCliente as empresacolonia,
        cli.ciudadCliente as empresaciudad,
        cli.estadoCliente as empresaestado,
        cli.codigoPostalCliente as codigoPostal,
        c.numero as cotizacionnumero,
        c.fechaSolicitud as cotizacionfecha,
        ic.mensajePropuesta as mensaje,
        s.nombreServicio as servicionombre,
        s.metodos_id as serviciometodoid,
        m.codigo as metodocodigo,
        cs.cantidad as serviciocantidad,
        cs.precio as servicioprecio,
        iv.porcentaje as iva,
        es.nombre as servicioestado,
        ic.termino as terminosycondiciones,
        ic.avisos as avisos,
        c.fechaCaducidad as cotizacionfechacaducidad,
        img.imagen as imagen,
        org.calle as calleorg,
        org.numero as numeroorg,
        org.colonia as coloniaorg,
        org.ciudad as ciudadorg,
        org.estado as estadoorg,
        org.codigoPostal as codigopostalorg,
        org.telefono as telefonoorg,
        org.pagina as paginaorg,
        us.first_name as usuarioNombre,
        us.last_name as usuarioApellido,
        c.descuento as cotizaciondescuento,
        tm.id as tipomonedaid,
        tm.codigo as tipomoneda,
        infs.tipoCambioDolar as tipocambio,
        cs.descripcion as descripcion,
        cli.division as division
    FROM core_cotizacion c
    LEFT JOIN core_cotizacionservicio cs ON c.id = cs.cotizacion_id
    LEFT JOIN core_servicio s ON cs.servicio_id = s.id
    LEFT JOIN core_metodos m ON s.metodos_id = m.id
    LEFT join core_cliente cli on c.cliente_id = cli.id
    LEFT JOIN core_titulo tit on cli.titulo_id = tit.id
    LEFT JOIN core_empresa emp ON cli.empresa_id = emp.id
    LEFT JOIN core_organizacion org ON emp.organizacion_id = org.id
    LEFT JOIN core_infocotizacion ic ON org.infoCotizacion_id = ic.id
    LEFT JOIN core_iva iv ON c.iva_id = iv.id
    LEFT JOIN core_estado es ON s.estado_id = es.id
    LEFT JOIN core_imagenmarcaagua img ON ic.imagenMarcaAgua_id = img.id
    LEFT JOIN core_user us ON org.id = us.organizacion_id
    LEFT JOIN core_infosistema infs ON org.infosistema_id = infs.id
    LEFT JOIN core_tipomoneda tm ON c.tipoMoneda_id = tm.id
    WHERE c.id = %s AND us.id = %s;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [cotizacion_id, user_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

    if not data:
        return HttpResponse("No se encontraron datos para la cotización especificada.", status=404)

    conceptos = []
    subtotal = Decimal(0)
    tipo_cambio = Decimal(data[0]['tipocambio']) if data[0]['tipomonedaid'] == 2 else Decimal(1)
    rounding = Decimal('0.01')

    for item in data:
        cantidad = Decimal(item['serviciocantidad'])
        precio = (Decimal(item['servicioprecio']) / tipo_cambio) \
            .quantize(rounding, rounding=ROUND_HALF_UP)
        subtotal_concepto = (cantidad * precio) \
                .quantize(rounding, rounding=ROUND_HALF_UP)
                
        precio_str    = f"{precio:,.2f}"       # => "1,234.50"
        subtotal_str  = f"{subtotal_concepto:,.2f}"  # => "12,345.67"

        conceptos.append({
            'nombre': item['servicionombre'],
            'descripcion': item['descripcion'],
            'metodo': item['metodocodigo'],
            'cantidad': f"{cantidad:,}", 
            'precio':precio_str,
            'subtotal':subtotal_str,
        })
        subtotal += subtotal_concepto
    
    descuento = Decimal(data[0]['cotizaciondescuento']) / Decimal(100)
    descuento_valor = (subtotal * descuento).quantize(rounding, rounding=ROUND_HALF_UP)
    subtotal_descuento = (subtotal - descuento_valor).quantize(rounding, rounding=ROUND_HALF_UP)
    iva_porcentaje = Decimal(data[0]['iva'])
    iva_valor = (subtotal_descuento * iva_porcentaje).quantize(rounding, rounding=ROUND_HALF_UP)
    total = (subtotal_descuento + iva_valor).quantize(rounding, rounding=ROUND_HALF_UP)

    # Construcción de URLs absolutas
    logo_url = request.build_absolute_uri(settings.MEDIA_URL + data[0]['logo'])
    marca_url = request.build_absolute_uri(settings.MEDIA_URL + data[0]['imagen'])

    context = {
        'org': data[0]['nombreOrganizacion'],
        'logo_url': logo_url,
        'marca': marca_url,
        'formato': {
            'nombre_formato': data[0]['nombreFormatoCotizacion'],
            'version': data[0]['versionFormatoCotizacion'],
            'fecha_emision': data[0]['fechaEmisionFormatoCotizacion'],
            'fecha_caducidad': data[0]['cotizacionfechacaducidad'],
        },
        'cliente': {
            'titulo': data[0]['tituloab'],
            'nombre': f"{data[0]['clientenombre']} {data[0]['clienteappaterno']}" + (f" {data[0]['clienterapmaterno']}" if data[0]['clienterapmaterno'] else ""),
            'empresa': data[0]['empresanombre'],
            'direccion': f"{data[0]['empresacalle']}, {data[0]['empresanumero']}, {data[0]['empresacolonia']}",
            'direccion2': f"{data[0]['empresaciudad']}, {data[0]['empresaestado']}, CP: {data[0]['codigoPostal']}",
            'division': data[0]['division'],
        },
        'organizacion': {
            'direccion': f"{data[0]['calleorg']} {data[0]['numeroorg']}, {data[0]['coloniaorg']}, {data[0]['ciudadorg']}, {data[0]['estadoorg']}, CP: {data[0]['codigopostalorg']}",
            'telefono': data[0]['telefonoorg'],
            'pagina': data[0]['paginaorg']
        },
        'cotizacion': {
            'numero': data[0]['cotizacionnumero'],
            'fecha': data[0]['cotizacionfecha'],
            'subtotal':f"{subtotal:,.2f}",
            'descuento': data[0]['cotizaciondescuento'],
            'descuento_valor':f"{descuento_valor:,.2f}",
            'subtotal_descuento':f"{subtotal_descuento:,.2f}",
            'iva':f"{iva_valor:,.2f}",
            'iva_porcentaje': data[0]['iva'],
            'total':f"{total:,.2f}",
            'fecha_caducidad': data[0]['cotizacionfechacaducidad'],
            'moneda': data[0]['tipomoneda'], 
        },
        'conceptos': conceptos,
        'terminos': data[0]['terminosycondiciones'],
        'avisos': data[0]['avisos'],
        'mensaje': data[0]['mensaje'],
        'current_date': datetime.now().strftime("%Y/%m/%d"),
        'usuario': f"{data[0]['usuarioNombre']} {data[0]['usuarioApellido']}",
    }

    html_string = render_to_string('cotizacion_plantilla.html', context)
    pdf = HTML(string=html_string).write_pdf()

    # Crear respuesta HTTP con el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="cotizacion_{cotizacion_id}.pdf"'
    return response

def generar_pdf_orden_trabajo(request, ordentrabajo_id):
    #permission_classes = [IsAuthenticated]
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return HttpResponse("Usuario no autenticado.", status=401)

    query = """
    SELECT
        org.logo as logo,
        org.nombre AS nombreOrganizacion,
        iot.`tituloDocumento` AS tituloDocumentoOrdenTrabajo,
        iot.`nombreFormato` AS nombreFormatoOrdenTrabajo,
        iot.`version` AS versionOrdenTrabajo,
        iot.`fechaEmision` AS fechaEmisionOrdenTrabajo,
        iot.`tituloDocumento` AS tituloDocumentoOrdenTrabajo,
        ot.codigo AS ordenTrabajoCodigo,
        emp.nombre as empresanombre,
        emp.rfc as empresarfc,
        cli.`nombrePila` as clientenombre,
        cli.`apPaterno` as clienteappaterno,
        cli.`apMaterno` as clienterapmaterno,
        cli.calleCliente as empresacalle,
        cli.numeroCliente as empresanumero,
        cli.coloniaCliente as empresacolonia,
        cli.ciudadCliente as empresaciudad,
        cli.estadoCliente as empresaestado,
        cli.`codigoPostalCliente` as codigoPostal,
        c.numero as cotizacionnumero,
        c.`fechaSolicitud` as cotizacionfecha,
        cli.celular as clientecelular,
        cli.telefono as clientetelefono,
        cli.correo as clientecorreo,
        s.`nombreServicio` as servicionombre,
        s.metodos_id as serviciometodoid,
        m.codigo as metodocodigo,
        ots.descripcion as serviciodescripcion,
        ots.cantidad as serviciocantidad,
        us.first_name as usuarioNombre,
        us.last_name as usuarioApellido,
        r.`nombrePila` as receptorNombre,
        r.`apPaterno` as receptorAppaterno,
        r.`apMaterno` as receptorApmaterno,
        img.imagen as imagenMarcaAgua,
        org.calle as calleorg,
        org.numero as numeroorg,
        org.colonia as coloniaorg,
        org.ciudad as ciudadorg,
        org.estado as estadoorg,
        org.`codigoPostal` as codigopostalorg,
        org.telefono as telefonoorg,
        org.pagina as paginaorg,
        cli.division as division
    from core_ordentrabajo ot
    LEFT JOIN core_cotizacion c ON ot.cotizacion_id = c.id
    LEFT JOIN core_ordentrabajoservicio ots ON ot.id = ots.ordenTrabajo_id
    LEFT JOIN core_servicio s ON ots.servicio_id = s.id
    LEFT join core_cliente cli on c.cliente_id = cli.id
    LEFT join core_empresa emp on cli.empresa_id = emp.id
    LEFT join core_organizacion org on emp.organizacion_id = org.id
    LEFT JOIN core_infoordentrabajo iot ON org.infoOrdenTrabajo_id = iot.id
    LEFT JOIN core_receptor r ON ot.receptor_id = r.id
    LEFT JOIN core_user us ON org.id = us.organizacion_id
    LEFT JOIN core_imagenmarcaagua img ON iot.imagenMarcaAgua_id = img.id
    LEFT JOIN core_metodos m ON s.metodos_id = m.id
    WHERE ot.id = %s AND us.id = %s;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [ordentrabajo_id, user_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

    conceptos = []
    for item in data:
        conceptos.append({
            'nombre': item['servicionombre'],
            'metodo': item['metodocodigo'],
            'cantidad': item['serviciocantidad'],
            'descripcion': item['serviciodescripcion'],
        })

    # Construcción de URLs absolutas
    logo_url = request.build_absolute_uri(settings.MEDIA_URL + data[0]['logo'])
    marca_url = request.build_absolute_uri(settings.MEDIA_URL + data[0]['imagenMarcaAgua'])

    context = {
        'org': data[0]['nombreOrganizacion'],
        'logo_url': logo_url,
        'marca': marca_url,
        'formato': {
            'nombre_formato': data[0]['nombreFormatoOrdenTrabajo'],
            'version': data[0]['versionOrdenTrabajo'],
            'fecha_emision': data[0]['fechaEmisionOrdenTrabajo'],
        },
        'cliente': {
            'empresa': data[0]['empresanombre'],
            'rfc': data[0]['empresarfc'],
            'nombre': f"{data[0]['clientenombre']} {data[0]['clienteappaterno']}" + (f" {data[0]['clienterapmaterno']}" if data[0]['clienterapmaterno'] else ""),
            'calle': data[0]['empresacalle'],
            'numero': data[0]['empresanumero'],
            'colonia': data[0]['empresacolonia'],
            'ciudad': data[0]['empresaciudad'],
            'estado': data[0]['empresaestado'],
            'codigo_postal': data[0]['codigoPostal'],
            'telefono': data[0]['clientetelefono'],
            'celular': data[0]['clientecelular'],
            'correo': data[0]['clientecorreo'],
            'division': data[0]['division'],
        },
        'organizacion': {
            'direccion': f"{data[0]['calleorg']} {data[0]['numeroorg']}, {data[0]['coloniaorg']}, {data[0]['ciudadorg']}, {data[0]['estadoorg']}, CP: {data[0]['codigopostalorg']}",
            'telefono': data[0]['telefonoorg'],
            'pagina': data[0]['paginaorg']
        },
        'orden_trabajo': {
            "cotizacion_id": data[0]['cotizacionnumero'],
            'codigo': data[0]['ordenTrabajoCodigo'],
            'fecha': data[0]['cotizacionfecha'],
        },
        'conceptos': conceptos,
        'current_date': datetime.now().strftime("%Y/%m/%d"),
        'usuario': f"{data[0]['usuarioNombre']} {data[0]['usuarioApellido']}",
        'receptor': {
            'nombre': f"{data[0]['receptorNombre']} {data[0]['receptorAppaterno']} {data[0]['receptorApmaterno']}",
        },
    }

    html_string = render_to_string('orden_trabajo_plantilla.html', context)
    pdf = HTML(string=html_string).write_pdf()

    # Crear respuesta HTTP con el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="orden_trabajo_{ordentrabajo_id}.pdf"'
    return response
    
class CurrencyView(APIView):
    #permission_classes = [IsAuthenticated]
    """
    Vista para obtener el catálogo de monedas aceptadas por la API de Facturama.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Obtener el parámetro 'keyword' de la solicitud (opcional)
            keyword = request.query_params.get('keyword', None)
            
            # URL para consultar el catálogo de monedas
            url = f"{SANDBOX_URL}/api/Catalogs/Currencies"
            
            # Parámetros de la solicitud
            params = {}
            if keyword:
                params['keyword'] = keyword
            
            # Realizar la solicitud a la API de Facturama
            response = requests.get(url, params=params, auth=(USERNAME, PASSWORD))
            
            # Imprimir la respuesta para depuración
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                # Devolver la lista de monedas en formato JSON
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                # Si la solicitud no fue exitosa, devolver un error con más detalles
                return Response(
                    {
                        "error": "No se pudo obtener el catálogo de monedas.",
                        "status_code": response.status_code,
                        "response_body": response.text
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            # Manejar cualquier excepción que ocurra durante la solicitud
            return Response(
                {"error": f"Error al consultar el catálogo de monedas: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
def enviar_pdf_cotizacion(request, cotizacion_id):
    #permission_classes = [IsAuthenticated]
    user_id = request.GET.get('user_id')

    if not user_id:
        return HttpResponse("Usuario no autenticado.", status=401)

    query = """
    SELECT cli.correo as cliente_email
    FROM core_cotizacion c
    LEFT JOIN core_cliente cli ON c.cliente_id = cli.id
    WHERE c.id = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [cotizacion_id])
        row = cursor.fetchone()

    if not row or not row[0]:  
        return HttpResponse("Correo electrónico no encontrado", status=400)

    cliente_email = row[0]

    # Obtener correos adicionales desde los parámetros de la solicitud
    correos_adicionales = request.GET.get('emails', '')  # Formato: email1,email2,email3
    lista_correos_adicionales = [email.strip() for email in correos_adicionales.split(',') if email.strip()]
    
    # Lista final de destinatarios
    destinatarios = [cliente_email] + lista_correos_adicionales

    # Generar el PDF incluyendo el user_id
    pdf_response = generar_pdf_cotizacion(request, cotizacion_id)
    pdf_bytes = pdf_response.content

    mensaje_correo = """\
    Buenas tardes, estimado cliente,

    Adjunto la cotización solicitada para su evaluación.

    Quedo a la espera de su respuesta para brindarle el seguimiento necesario.

    Saludos, quedo a su disposición para cualquier duda o comentario adicional.

    Le agradecería confirmar la recepción de este correo y verificar si los datos de la cotización son correctos.
    Si requiere alguna modificación, por favor házmelo saber para realizar el ajuste de inmediato.
    """

    # Crear y enviar el correo
    email = EmailMessage(
        subject=f"Cotización #{cotizacion_id}",
        body=mensaje_correo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios
    )

    email.attach(f'cotizacion_{cotizacion_id}.pdf', pdf_bytes, 'application/pdf')
    email.send()

    return HttpResponse(f"Correo enviado a: {', '.join(destinatarios)}", status=200)

def factura_pdf_enviar(request, factura_id):
    #permission_classes = [IsAuthenticated]
    query = """
    SELECT cli.correo as clientecorreo
    FROM core_factura f
    LEFT JOIN core_ordentrabajo ot ON f.ordenTrabajo_id = ot.id
    LEFT JOIN core_cotizacion c ON ot.cotizacion_id = c.id
    LEFT JOIN core_cliente cli ON c.cliente_id = cli.id
    WHERE f.id = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [factura_id])
        row = cursor.fetchone()

    if not row or not row[0]:  
        return HttpResponse("Correo electrónico del cliente no encontrado", status=400)

    cliente_email = row[0]

    # Obtener correos adicionales (si existen) desde la URL
    emails_adicionales = request.GET.get("emails", "")
    if emails_adicionales:
        # Convertir la cadena de correos adicionales en una lista
        emails_adicionales = emails_adicionales.split(",")
    else:
        emails_adicionales = []

    # Buscar el idfactura en FacturaFacturama
    try:
        factura_facturama = FacturaFacturama.objects.get(factura_id=factura_id)
    except FacturaFacturama.DoesNotExist:
        return JsonResponse({"error": "El factura_id proporcionado no existe en FacturaFacturama."}, status=404)
    
    id_factura = factura_facturama.idfactura

    # Obtener el PDF desde Facturama
    url = f"{settings.SANDBOX_URL}/cfdi/pdf/issuedLite/{id_factura}"
    response = requests.get(url, auth=(settings.USERNAME, settings.PASSWORD))

    if response.status_code != 200:
        return JsonResponse({"error": f"Error al obtener el PDF de Facturama: {response.text}"}, status=response.status_code)

    pdf_data = response.json()

    # Validar si el contenido es un PDF en Base64
    if "Content" not in pdf_data or "ContentType" not in pdf_data or pdf_data["ContentType"] != "pdf":
        return JsonResponse({"error": "El contenido del PDF no está disponible o es inválido."}, status=400)

    pdf_content = base64.b64decode(pdf_data["Content"])

    # Mensaje del correo
    mensaje_correo = f"""\
    Buenas tardes, estimado cliente,

    Adjunto la factura correspondiente a su orden.

    Quedo a la espera de su confirmación de recepción y a su disposición para cualquier duda o comentario adicional.

    Si encuentra alguna discrepancia en la factura, por favor notifíqueme de inmediato para realizar los ajustes necesarios.

    Saludos cordiales.
    """

    destinatarios = [cliente_email] + emails_adicionales

    email = EmailMessage(
        subject=f"Factura #{factura_id}",
        body=mensaje_correo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios
    )

    email.attach(f'factura_{factura_id}.pdf', pdf_content, 'application/pdf')
    email.send()

    return HttpResponse(f"Factura enviada por correo a {', '.join(destinatarios)}", status=200)

def generar_pdf_precotizacion(request, precotizacion_id):
    #permission_classes = [IsAuthenticated]
    user_id = request.GET.get('user_id')
    organizacion_id = request.GET.get('organizacion_id')
    
    if not user_id or not organizacion_id:
        return HttpResponse("Faltan parámetros: user_id y/o organizacion_id", status=400)
    
    # Consulta SQL adaptada para pre-cotización, similar a la de cotización
    query = """
    SELECT
        cp.id AS precotizacionnumero,
        cp.nombreEmpresa AS empresanombre,
        cp.nombreCliente AS clientenombre,
        cp.apellidoCliente AS clienterapellido,
        cp.correo as clientecorreo,
        cp.fechaSolicitud AS precotizacionfecha,
        cp.fechaCaducidad AS precotizacionfechacaducidad,
        cp.descuento AS precotizaciondescuento,
        iv.porcentaje AS iva,
        tm.id AS tipomonedaid,
        tm.codigo AS tipomoneda,
        s.nombreServicio AS servicionombre,
        m.codigo AS metodocodigo,
        cps.cantidad AS serviciocantidad,
        cps.precio AS servicioprecio,
        cps.descripcion AS descripcion,
        org.logo AS logo,
        org.nombre AS nombreOrganizacion,
        org.calle AS calleorg,
        org.numero AS numeroorg,
        org.colonia AS coloniaorg,
        org.ciudad AS ciudadorg,
        org.estado AS estadoorg,
        org.codigoPostal AS codigopostalorg,
        org.telefono AS telefonoorg,
        org.pagina AS paginaorg,
        ic.nombreFormato AS nombreFormatoPrecotizacion,
        ic.version AS versionFormatoPrecotizacion,
        ic.fechaEmision AS fechaEmisionFormatoPrecotizacion,
        ic.tituloDocumento AS tituloDocumentoPrecotizacion,
        ic.mensajePropuesta AS mensaje,
        ic.termino AS terminosycondiciones,
        ic.avisos AS avisos,
        infs.tipoCambioDolar AS tipocambio,
        us.first_name AS usuarioNombre,
        us.last_name AS usuarioApellido,
        img.imagen as imagenMarcaAgua
    FROM core_precotizacion cp
    LEFT JOIN core_precotizacionservicio cps ON cp.id = cps.preCotizacion_id
    LEFT JOIN core_servicio s ON cps.servicio_id = s.id
    LEFT JOIN core_metodos m ON s.metodos_id = m.id
    LEFT JOIN core_iva iv ON cp.iva_id = iv.id
    LEFT JOIN core_tipomoneda tm ON cp.tipoMoneda_id = tm.id
    -- Inyectamos la organización mediante CROSS JOIN para poder usar sus datos en joins posteriores
    CROSS JOIN core_organizacion org
    LEFT JOIN core_infocotizacion ic ON org.infoCotizacion_id = ic.id
    LEFT JOIN core_imagenmarcaagua img ON ic.imagenMarcaAgua_id = img.id
    LEFT JOIN core_user us ON org.id = us.organizacion_id
    LEFT JOIN core_infosistema infs ON org.infosistema_id = infs.id
    WHERE cp.id = %s
      AND us.id = %s
      AND org.id = %s;
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [precotizacion_id, user_id, organizacion_id])
        rows = cursor.fetchall()
        if not rows:
            return HttpResponse("No se encontraron datos para la pre-cotización especificada.", status=404)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

    # Procesamos los servicios asociados y calculamos totales similares a la cotización
    conceptos = []
    subtotal = Decimal(0)
    # Se utiliza el tipo de cambio solo si la moneda es distinta a la base (por ejemplo, 2 = dólar)
    tipo_cambio = Decimal(data[0]['tipocambio']) if data[0]['tipomonedaid'] == 2 else Decimal(1)
    rounding = Decimal('0.01')

    for item in data:
        cantidad = Decimal(item['serviciocantidad'])
        precio = (Decimal(item['servicioprecio']) / tipo_cambio).quantize(rounding, rounding=ROUND_HALF_UP)
        subtotal_concepto = (cantidad * precio).quantize(rounding, rounding=ROUND_HALF_UP)
        conceptos.append({
            'nombre': item['servicionombre'],
            'metodo': item['metodocodigo'],
            'cantidad': cantidad,
            'precio': precio,
            'subtotal': subtotal_concepto,
            'descripcion': item['descripcion']
        })
        subtotal += subtotal_concepto

    descuento = Decimal(data[0]['precotizaciondescuento']) / Decimal(100)
    descuento_valor = (subtotal * descuento).quantize(rounding, rounding=ROUND_HALF_UP)
    subtotal_descuento = (subtotal - descuento_valor).quantize(rounding, rounding=ROUND_HALF_UP)
    iva_porcentaje = Decimal(data[0]['iva'])
    iva_valor = (subtotal_descuento * iva_porcentaje).quantize(rounding, rounding=ROUND_HALF_UP)
    total = (subtotal_descuento + iva_valor).quantize(rounding, rounding=ROUND_HALF_UP)

    # Construcción de URLs absolutas para imágenes
    logo_url = request.build_absolute_uri(settings.MEDIA_URL + data[0]['logo'])
    marca_url = request.build_absolute_uri(settings.MEDIA_URL + data[0]['imagenMarcaAgua'])
    
    
    # Armamos el contexto similar al de cotización, adaptando los nombres de campos
    context = {
        'org': data[0]['nombreOrganizacion'],
        'logo_url': logo_url,
        'marca': marca_url,
        'formato': {
            'nombre_formato': data[0]['nombreFormatoPrecotizacion'],
            'version': data[0]['versionFormatoPrecotizacion'],
            'fecha_emision': data[0]['fechaEmisionFormatoPrecotizacion'],
            'fecha_caducidad': data[0]['precotizacionfechacaducidad'],  # O bien otro campo, según convenga
            'titulo_documento': data[0]['tituloDocumentoPrecotizacion'],
        },
        'cliente': {
            # En precotización los datos del cliente se almacenan en atributos
            'nombre': f"{data[0]['clientenombre']} {data[0]['clienterapellido']}",
            'empresa': data[0]['empresanombre'],
        },
        'organizacion': {
            'direccion': f"{data[0]['calleorg']} {data[0]['numeroorg']}, {data[0]['coloniaorg']}, {data[0]['ciudadorg']}, {data[0]['estadoorg']}, CP: {data[0]['codigopostalorg']}",
            'telefono': data[0]['telefonoorg'],
            'pagina': data[0]['paginaorg']
        },
        'precotizacion': {
            'numero': data[0]['precotizacionnumero'],
            'fecha': data[0]['precotizacionfecha'],
            'subtotal': subtotal,
            'descuento': data[0]['precotizaciondescuento'],
            'descuento_valor': descuento_valor,
            'subtotal_descuento': subtotal_descuento,
            'iva': iva_valor,
            'iva_porcentaje': data[0]['iva'],
            'total': total,
            'fecha_caducidad': data[0]['precotizacionfechacaducidad'],
            'moneda': data[0]['tipomoneda'], 
        },
        'conceptos': conceptos,
        'terminos': data[0]['terminosycondiciones'],
        'avisos': data[0]['avisos'],
        'mensaje': data[0]['mensaje'],
        'current_date': datetime.now().strftime("%Y/%m/%d"),
        'usuario': f"{data[0]['usuarioNombre']} {data[0]['usuarioApellido']}",
    }

    html_string = render_to_string('precotizacion_plantilla.html', context)
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="precotizacion_{precotizacion_id}.pdf"'
    return response

def enviar_pdf_precotizacion(request, precotizacion_id):
    #permission_classes = [IsAuthenticated]
    user_id = request.GET.get('user_id')
    organizacion_id = request.GET.get('organizacion_id')

    if not user_id or not organizacion_id:
        return HttpResponse("Usuario y/o organización no autenticados.", status=401)

    # Consulta para obtener el correo del cliente asociado a la precotización
    query = """
    SELECT cp.correo as clientecorreo
    FROM core_precotizacion cp
    WHERE cp.id = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [precotizacion_id])
        row = cursor.fetchone()

    if not row or not row[0]:
        return HttpResponse("Correo electrónico no encontrado.", status=400)

    client_email = row[0]

    # Obtener correos adicionales desde los parámetros de la solicitud (formato: email1,email2,...)
    correos_adicionales = request.GET.get('emails', '')
    lista_correos_adicionales = [email.strip() for email in correos_adicionales.split(',') if email.strip()]

    # Lista final de destinatarios
    destinatarios = [client_email] + lista_correos_adicionales

    # Generar el PDF de la pre-cotización (la función ya espera user_id y organizacion_id en GET)
    pdf_response = generar_pdf_precotizacion(request, precotizacion_id)
    pdf_bytes = pdf_response.content

    mensaje_correo = """\
Buenas tardes, estimado cliente,

Adjunto la cotización solicitada para su evaluación.

Quedo a la espera de su respuesta para brindarle el seguimiento necesario.

Saludos, quedo a su disposición para cualquier duda o comentario adicional.

Le agradecería confirmar la recepción de este correo y verificar si los datos de la cotización son correctos.
Si requiere alguna modificación, por favor házmelo saber para realizar el ajuste de inmediato.
    """

    # Crear y enviar el correo electrónico
    email = EmailMessage(
        subject=f"Cotización #{precotizacion_id}",
        body=mensaje_correo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios
    )

    email.attach(f'precotizacion_{precotizacion_id}.pdf', pdf_bytes, 'application/pdf')
    email.send()

    return HttpResponse(f"Correo enviado a: {', '.join(destinatarios)}", status=200)

def get_complemento_pago(request, comprobante_pago_id):
    #permission_classes = [IsAuthenticated]
    from django.db import connection
    from django.http import JsonResponse
    from decimal import Decimal, ROUND_HALF_UP

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                cp.numero as folio,
                org.nombre as nombreIssuer,
                rg.codigo as regimenFiscal,
                org.`codigoPostal` as codigopostalIssuer,
                csdl.rfc as rfcissuer,
                emp.rfc as rfcereceiver,
                emp.nombre as nombreEmpresa,
                rf_emp.codigo as regimenFiscal_id,
                emp.`codigoPostal` as codigoPostalempresa,
                cp.fechaPago AS fechaPago,
                f.numero AS foliofactura,
                cpf.montototal AS montoTotal,
                cpf.montorestante AS montoRestante,
                cpf.montopago AS montoPago,
                ff.uuid AS uuid,
                ff.factura_id AS factura_id,
                cp.observaciones AS observaciones,
                iv.porcentaje AS iva,
                tm.codigo AS codigotipomoneda,
                cpf.parcialidad AS parcialidad,
                fp.codigo AS formaPago_id,
                infs.`tipoCambioDolar` AS tipocambio,
                org.logo as logo
            FROM core_comprobantepago cp
            LEFT JOIN core_comprobantepagofactura cpf ON cp.id = cpf.comprobantePago_id
            LEFT JOIN core_factura f ON cpf.factura_id = f.id
            LEFT JOIN core_facturafacturama ff ON f.id = ff.factura_id
            LEFT JOIN core_cotizacion c ON f.cotizacion_id = c.id
            LEFT JOIN core_cliente cli ON c.cliente_id = cli.id
            LEFT JOIN core_empresa emp ON cli.empresa_id = emp.id
            LEFT JOIN core_organizacion org ON emp.organizacion_id = org.id
            LEFT JOIN core_regimenfiscal rg on org.regimenFiscal_id = rg.id
            LEFT JOIN core_regimenfiscal rf_emp ON emp.regimenFiscal_id = rf_emp.id
            LEFT JOIN core_certificadosellodigital csdl ON org.id = csdl.Organizacion_id
            LEFT JOIN core_iva iv ON c.iva_id = iv.id
            LEFT JOIN core_tipomoneda tm ON c.tipoMoneda_id = tm.id
            LEFT JOIN core_formapago fp ON cp.formaPago_id = fp.id
            LEFT JOIN core_infosistema infs ON org.infosistema_id = infs.id
            WHERE cp.id = %s;
        """, [comprobante_pago_id])
        rows = cursor.fetchall()

    if not rows:
        return JsonResponse({
            "error": "No se encontraron datos para el comprobante de pago especificado."
        })

    # Usar la primera fila para los datos comunes
    common = rows[0]
    voucher_id          = common[0]  # cp.id
    nombreIssuer        = common[1]  # org.nombre
    regimenFiscal       = common[2]  # rg.codigo
    codigopostalIssuer  = common[3]  # org.codigoPostal
    rfcissuer           = common[4]  # csdl.rfc
    rfcereceiver        = common[5]  # emp.rfc
    nombreEmpresa       = common[6]  # emp.nombre
    regimenFiscal_id    = common[7]  # rf_emp.codigo
    codigoPostalempresa = common[8]  # emp.codigoPostal
    fechaPago           = common[9]  # cp.fechaPago
    observaciones       = common[16]  # cp.observaciones

    tijuana_tz = pytz.timezone("America/Tijuana")
    today = datetime.now(tijuana_tz).date()  # fecha de hoy
    hora_fija = time(0, 0, 0)                # 00:00:00
    fechaPago_iso = datetime.combine(today, hora_fija).isoformat()
    fechaPago_date = fechaPago.date().isoformat()

    total_monto_pago = Decimal('0.00')
    related_documents = []

    for row in rows:
        foliofactura      = row[10]   # f.id
        montoTotal        = row[11]   # cpf.montototal
        montoRestante     = row[12]   # cpf.montorestante
        montoPago         = row[13]   # cpf.montopago
        uuid_val          = row[14]   # ff.uuid
        iva               = row[17]   # iv.porcentaje
        tipomoneda        = row[18]   # tm.codigo
        parcialidad       = row[19]   # cpf.parcialidad
        formapago         = row[20]   # fp.codigo
        tipocambiodolar   = row[21]   # infs.tipoCambioDolar

        total_monto_pago += Decimal(montoPago)

        # Calcular el desglose de IVA (montoPago ya lo incluye)
        tax_rate = Decimal(iva)
        # Si la tasa se almacena en porcentaje (por ejemplo, 16), convertir a decimal (0.16)
        if tax_rate > Decimal('1'):
            tax_rate = tax_rate / Decimal('100')
        # Calcular la base y el IVA a partir del monto pagado
        base_amount = Decimal(montoPago) / (Decimal('1') + tax_rate)
        tax_amount = Decimal(montoPago) - base_amount

        # Redondear a dos decimales
        base_amount = base_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        tax_amount = tax_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        related_doc = {
            "TaxObject": "02",
            "Uuid": uuid_val,
            "Serie": "FAC",  # Ajusta la serie si es necesario
            "Folio": str(foliofactura),
            "Currency": tipomoneda,
            "EquivalenceDocRel": 1,
            "PaymentMethod": "PPD",
            "PartialityNumber": parcialidad,
            "PreviousBalanceAmount": str(montoTotal),
            "AmountPaid": str(montoPago),
            "ImpSaldoInsoluto": str(montoRestante),
            "Taxes": [
                {
                    "Total": str(tax_amount),
                    "Name": "IVA",
                    "Base": str(base_amount),
                    "Rate": float(round(tax_rate, 6)),
                    "IsRetention": False
                }
            ]
        }
        related_documents.append(related_doc)

    # Construir el diccionario de Payment condicionalmente
    payment_data = {
        "Date": fechaPago_date,
        "PaymentForm": formapago,
        "Amount": str(total_monto_pago),
        "Currency": tipomoneda,
        "RelatedDocuments": related_documents
    }
    # Si la moneda no es MXN, incluir el tipo de cambio
    if tipomoneda != "MXN":
        payment_data["ExchangeRate"] = tipocambiodolar

    complemento_pago = {
        "NameId": "14",
        "Folio": str(voucher_id),
        "CfdiType": "P",
        "ExpeditionPlace": codigopostalIssuer,
        "Date": fechaPago_iso,
        "Observations": observaciones,
        "LogoUrl": "https://api.simplaxi.com/media/" + common[22],
        "Exportation": "01",
        "Issuer": {
            "Rfc": rfcissuer,
            "Name": nombreIssuer,
            "FiscalRegime": regimenFiscal
        },
        "Receiver": {
            "Rfc": rfcereceiver,
            "CfdiUse": "CP01",
            "Name": nombreEmpresa,
            "FiscalRegime": str(regimenFiscal_id),
            "TaxZipCode": codigoPostalempresa
        },
        "Complemento": {
            "Payments": [payment_data]
        }
    }


    # Llamada a la API de Facturama
    response = crear_cfdi_api(complemento_pago)

    # 7) Manejar respuesta
    comp = response.get("Complement", {})
    if response.get("Id") and comp.get("TaxStamp", {}).get("Uuid"):
        # Guardar facturama_id en ComprobantePago
        comprobante = get_object_or_404(ComprobantePago, pk=comprobante_pago_id)
        comprobante.facturama_id = response["Id"]
        comprobante.save()

        # Registrar cada factura en FacturaFacturama
        for row in rows:
            FacturaFacturama.objects.create(
                uuid=row[14],
                idfactura=row[10]
            )
        return JsonResponse({"success": True, "cfdi": response})

    # 8) Si no fue exitoso, devolver error JSON
    return JsonResponse({
        "error":     "No se pudo generar el complemento de pago.",
        "response":  response
    }, status=400)
def comprobante_pdf(request, comprobante_id):
    #permission_classes = [IsAuthenticated]
    try:
        # Buscar el registro en Comprobante usando su ID
        try:
            comprobante = ComprobantePago.objects.get(id=comprobante_id)
        except ComprobantePago.DoesNotExist:
            return JsonResponse({"error": "El comprobante_id proporcionado no existe en Comprobante."}, status=404)

        # Obtener el ID de Facturama (facturama_id)
        facturama_id = comprobante.facturama_id
        
        if not facturama_id:
            return JsonResponse({"error": "No se encontró un ID de Facturama para este comprobante."}, status=400)
        # URL para obtener el PDF del comprobante
        url = f"{SANDBOX_URL}/cfdi/pdf/issuedLite/{facturama_id}"
        response = requests.get(url, auth=(USERNAME, PASSWORD))
        if response.status_code == 200:
            pdf_data = response.json()

            if "Content" in pdf_data and "ContentType" in pdf_data and pdf_data["ContentType"] == "pdf":
                pdf_content = base64.b64decode(pdf_data["Content"])
                response = HttpResponse(pdf_content, content_type="application/pdf")
                response["Content-Disposition"] = f"attachment; filename=comprobante_{comprobante_id}.pdf"
                return response
            else:
                return JsonResponse({"error": "El contenido del PDF no está disponible o es inválido."}, status=400)
        else:
            return JsonResponse({"error": f"Error al obtener el PDF del comprobante: {response.text}"}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": f"Error al procesar la solicitud: {str(e)}"}, status=500)
    
def comprobante_xml(request, comprobante_id):
    #permission_classes = [IsAuthenticated]
    try:
        # Buscar el registro en Comprobante usando su ID
        try:
            comprobante = ComprobantePago.objects.get(id=comprobante_id)
        except ComprobantePago.DoesNotExist:
            return JsonResponse({"error": "El comprobante_id proporcionado no existe en Comprobante."}, status=404)

        # Obtener el ID de Facturama (facturama_id)
        facturama_id = comprobante.facturama_id
        
        if not facturama_id:
            return JsonResponse({"error": "No se encontró un ID de Facturama para este comprobante."}, status=400)
        # URL para obtener el PDF del comprobante
        url = f"{SANDBOX_URL}/cfdi/xml/issuedLite/{facturama_id}"
        response = requests.get(url, auth=(USERNAME, PASSWORD))
        if response.status_code == 200:
            xml_data = response.json()

            # Verificar si el contenido está codificado en Base64
            if "Content" in xml_data and "ContentType" in xml_data and xml_data["ContentType"] == "xml":
                xml_content = base64.b64decode(xml_data["Content"])

                # Crear la respuesta de archivo XML
                response = HttpResponse(xml_content, content_type="application/xml")
                response["Content-Disposition"] = f"attachment; filename=comprobante_{comprobante_id}.xml"
                return response
            else:
                return JsonResponse({"error": "El contenido del XML no está disponible o es inválido."}, status=400)
        else:
            return JsonResponse({"error": f"Error al obtener el XML de Facturama: {response.text}"}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": f"Error al procesar la solicitud: {str(e)}"}, status=500)
    
def comprobante_pdf_enviar(request, comprobante_id):
    #permission_classes = [IsAuthenticated]
    query = """
    SELECT cli.correo as clientecorreo
    FROM core_comprobantepago cp
    LEFT JOIN core_comprobantepagofactura cpf ON cp.id = cpf.comprobantePago_id
    LEFT JOIN core_factura f ON cpf.factura_id = f.id
    LEFT JOIN core_ordentrabajo ot ON f.ordenTrabajo_id = ot.id
    LEFT JOIN core_cotizacion c ON ot.cotizacion_id = c.id
    LEFT JOIN core_cliente cli ON c.cliente_id = cli.id
    WHERE cp.id = %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [comprobante_id])
        row = cursor.fetchone()
    
    if not row or not row[0]:
        return HttpResponse("Correo electrónico del cliente no encontrado", status=400)
    
    cliente_email = row[0]

    # 2. Obtener correos adicionales (si se pasan en la URL, separados por comas)
    emails_adicionales = request.GET.get("emails", "")
    if emails_adicionales:
        emails_adicionales = emails_adicionales.split(",")
    else:
        emails_adicionales = []

    # 3. Buscar el comprobante en la base de datos
    try:
        comprobante = ComprobantePago.objects.get(id=comprobante_id)
    except ComprobantePago.DoesNotExist:
        return JsonResponse({"error": "El comprobante_id proporcionado no existe en Comprobante."}, status=404)
    
    # 4. Obtener el ID de Facturama para el comprobante
    facturama_id = comprobante.facturama_id
    if not facturama_id:
        return JsonResponse({"error": "No se encontró un ID de Facturama para este comprobante."}, status=400)

    # 5. Obtener el PDF desde Facturama
    url = f"{settings.SANDBOX_URL}/cfdi/pdf/issuedLite/{facturama_id}"
    response = requests.get(url, auth=(settings.USERNAME, settings.PASSWORD))
    if response.status_code != 200:
        return JsonResponse({"error": f"Error al obtener el PDF del comprobante: {response.text}"}, status=response.status_code)
    
    pdf_data = response.json()
    if "Content" not in pdf_data or "ContentType" not in pdf_data or pdf_data["ContentType"] != "pdf":
        return JsonResponse({"error": "El contenido del PDF no está disponible o es inválido."}, status=400)
    
    pdf_content = base64.b64decode(pdf_data["Content"])

    # 6. Preparar el mensaje del correo
    mensaje_correo = (
        "Buenas tardes, estimado cliente,\n\n"
        "Adjunto el comprobante de pago correspondiente a su operación.\n\n"
        "Quedo a la espera de su confirmación de recepción y a su disposición para cualquier duda o comentario adicional.\n\n"
        "Saludos cordiales."
    )

    destinatarios = [cliente_email] + emails_adicionales

    # 7. Enviar el correo con el PDF adjunto
    email = EmailMessage(
        subject=f"Complemento de pago #{comprobante_id}",
        body=mensaje_correo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=destinatarios
    )
    email.attach(f'comprobante_{comprobante_id}.pdf', pdf_content, 'application/pdf')
    email.send()

    return HttpResponse(f"Comprobante de pago enviado por correo a {', '.join(destinatarios)}", status=200)
    
def cancelar_comprobante_api(facturama_id):
    """
    Cancela un comprobante de pago en la API de Facturama usando facturama_id.
    """
    url = f"{SANDBOX_URL}/api-lite/cfdis/{facturama_id}"
    try:
        response = requests.delete(url, auth=(USERNAME, PASSWORD))
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json() if response.content else f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def comprobante_delete(request, comprobante_id):
    """
    Si el comprobante NO tiene facturama_id, lo elimina de la base de datos.
    Si tiene facturama_id, primero lo cancela en la API y luego lo elimina.
    """
    try:
        comprobante = ComprobantePago.objects.get(id=comprobante_id)

        if comprobante.facturama_id:
            # Si tiene facturama_id, primero intenta cancelarlo en Facturama
            success, response = cancelar_comprobante_api(comprobante.facturama_id)
            if not success:
                return JsonResponse({"error": "Error al cancelar el comprobante.", "response": response}, status=400)

        # Si no tiene facturama_id o la cancelación fue exitosa, se elimina de la BD
        comprobante.delete()
        return JsonResponse({"success": "Comprobante eliminado exitosamente."})

    except ComprobantePago.DoesNotExist:
        return JsonResponse({"error": "El comprobante no existe."}, status=404)

def obtener_csd(request, organizacion_id):
    try:
        csds = CertificadoSelloDigital.objects.filter(Organizacion_id=organizacion_id).values('rfc', 'archivocer', 'archivokey')
        return JsonResponse(list(csds), safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from core.models import (
    PreCotizacion, PreCotizacionServicio,
    Empresa, Cliente,
    Cotizacion, CotizacionServicio,
    Estado
)
from core.serializers import CotizacionSerializer

@api_view(['GET'])
def pasarprecotizacion(request, id):
    """
    Convierte una PreCotizacion (cuando su estado_id == 7) en una Cotizacion "consecutiva":
    - Busca o crea Empresa
    - Busca o crea Cliente
    - Crea Cotizacion (numero se calcula en save())
    - Copia todos los servicios de la precotización
    """
    try:
        precot = PreCotizacion.objects.get(pk=id)
    except PreCotizacion.DoesNotExist:
        return Response({'detail': 'PreCotizacion no encontrada.'},
                        status=status.HTTP_404_NOT_FOUND)

    # Sólo procesar si el estado es el que indica "pasar a cotización"
    if precot.estado_id != 8:
        return Response(
            {'detail': f'El estado actual ({precot.estado_id}) no permite pasar a cotización.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    with transaction.atomic():
        # 1) Empresa: get_or_create()
        empresa, creada_empresa = Empresa.objects.get_or_create(
            nombre       = precot.nombreEmpresa,
            organizacion = precot.organizacion,
            defaults={
                'rfc': '',
                'codigoPostal': '',
                'ciudad': '',
                'estado': '',
                'colonia': '',
                'numeroExterior': '',
                'calle': '',
                'UsoCfdi_id': None,
                'regimenFiscal_id': None,
            }
        )

        # 2) Cliente: get_or_create()
        cliente, creada_cliente = Cliente.objects.get_or_create(
            nombrePila = precot.nombreCliente,
            apPaterno  = precot.apellidoCliente,
            empresa    = empresa,
            defaults={
                'apMaterno': '',
                'correo': precot.correo or '',
                'telefono': '',
                'celular': '',
                'fax': '',
                'titulo_id': None,
            }
        )

        # 3) Cotización nueva
        #    Estado "1" aquí equivale al estado por defecto de una cotización recién creada
        estado_por_defecto = Estado.objects.get(pk=1)
        cot = Cotizacion(
            denominacion     = precot.denominacion,
            fechaSolicitud   = precot.fechaSolicitud,
            fechaCaducidad   = precot.fechaCaducidad,
            descuento        = precot.descuento,
            iva_id           = precot.iva_id,
            estado           = estado_por_defecto,
            cliente          = cliente,
            tipoMoneda_id    = precot.tipoMoneda_id,
        )
        cot.save()  # aquí se calcula y asigna el número consecutivo

        # 4) Copiar servicios
        detalles = PreCotizacionServicio.objects.filter(preCotizacion=precot)
        for item in detalles:
            CotizacionServicio.objects.create(
                descripcion  = item.descripcion,
                precio       = item.precio,
                cotizacion   = cot,
                servicio_id  = item.servicio_id,
                cantidad     = item.cantidad,
            )

    # Serializar y devolver la cotización creada
    serializer = CotizacionSerializer(cot)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
