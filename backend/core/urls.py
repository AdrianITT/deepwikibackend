from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegimenFiscalViewSet, TipoMonedaViewSet, IvaViewSet, ImagenMarcaAguaViewSet, RolViewSet
from .views import TituloViewSet, UnidadCfdiViewSet, MetodosViewSet, ClaveCfdiViewSet, ObjetoImpuestoViewSet
from .views import EstadoViewSet, ReceptorViewSet, InfoOrdenTrabajoViewSet, InfoCotizacionViewSet
from .views import InfoSistemaViewSet, OrganizacionViewSet, EmpresaViewSet, ClienteViewSet, ServicioViewSet
from .views import CotizacionViewSet, OrdenTrabajoViewSet, FacturaViewSet, FacturaServicioViewSet
from .views import CertificadoSelloDigitalViewSet, UserViewSet, OrdenTrabajoServicioViewSet
from .views import FacturaFacturamaViewSet, CotizacionServicioViewSet, ComprobantePagoFacturaViewSet
from .views import get_factura_data, carga_csd, factura_detail, factura_delete, enviar_pdf_cotizacion
from .views import factura_pdf, factura_xml, CustomAuthToken, LogoutView, factura_pdf_enviar, borrar_csd
from .views import generar_pdf_cotizacion, generar_pdf_orden_trabajo, CurrencyView
from .views import TipoCfdiViewSet, FormaPagoViewSet, MetodoPagoViewSet, UsoCfdiViewSet
from .views import PreCotizacionViewSet, PreCotizacionServicioViewSet, ComprobantePagoViewSet, obtener_csd
from .views import generar_pdf_precotizacion, enviar_pdf_precotizacion, get_complemento_pago, comprobante_pdf, comprobante_pdf_enviar
from .views import pagosFactura, comprobante_delete, pasarprecotizacion, comprobante_xml
from .customViews.cotizacion.views import duplicarCotizacion, detalleCotizacionData, allcotizacionesdata, contar_cotizaciones, crearOrdenTrabajo, crearFactura
from .customViews.ordenTrabajo.views import dataOrdenTrabajo, allOrdenTrabajoData, dataOrdenTrabajoCrearFactura, dataEditOrdenTrabajo
from .customViews.cliente.views import direccionclienteempresa, editcliente, clienteFactura, clienteConFactura, listaClientes, allClientesData
from .customViews.factura.views import allfacturasdata, detalleFacturaData, facturaCliente, facturaMontoTotal
from .customViews.preCotizacion.views import allPrecotizacionData, detallePreCotizacionData
from .customViews.comprobantePago.views import allcomprobantepagodata
from .customViews.metodo.views import allMetodosData
from .customViews.servicio.views import allServiciosData
from .customViews.empresa.views import allEmpresasData

router = DefaultRouter()
router.register(r'regimenfiscal', RegimenFiscalViewSet)
router.register(r'tipomoneda', TipoMonedaViewSet)
router.register(r'iva', IvaViewSet)
router.register(r'imagenmarcaagua', ImagenMarcaAguaViewSet)
router.register(r'rol', RolViewSet)
router.register(r'user', UserViewSet)
router.register(r'titulo', TituloViewSet)
router.register(r'unidadcfdi', UnidadCfdiViewSet)
router.register(r'metodos', MetodosViewSet)
router.register(r'clavecdfi', ClaveCfdiViewSet)
router.register(r'objetoimpuesto', ObjetoImpuestoViewSet)
router.register(r'estado', EstadoViewSet)
router.register(r'tipocfdi', TipoCfdiViewSet)
router.register(r'formapago', FormaPagoViewSet)
router.register(r'metodopago', MetodoPagoViewSet)
router.register(r'usocfdi', UsoCfdiViewSet)
router.register(r'receptor', ReceptorViewSet)
router.register(r'infoordentrabajo', InfoOrdenTrabajoViewSet)
router.register(r'infocotizacion', InfoCotizacionViewSet)
router.register(r'infosistema', InfoSistemaViewSet)
router.register(r'organizacion', OrganizacionViewSet)
router.register(r'empresa', EmpresaViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'servicio', ServicioViewSet)
router.register(r'cotizacion', CotizacionViewSet)
router.register(r'cotizacionservicio', CotizacionServicioViewSet)
router.register(r'precotizacion', PreCotizacionViewSet)
router.register(r'precotizacionservicio', PreCotizacionServicioViewSet)
router.register(r'ordentrabajo', OrdenTrabajoViewSet)
router.register(r'ordentrabajoservicio', OrdenTrabajoServicioViewSet)
router.register(r'factura', FacturaViewSet)
router.register(r'facturaservicio', FacturaServicioViewSet)
router.register(r'certificadosellodigital', CertificadoSelloDigitalViewSet)
router.register(r'facturafacturama', FacturaFacturamaViewSet)
router.register(r'comprobantepago', ComprobantePagoViewSet)
router.register(r'comprobantepagofactura', ComprobantePagoFacturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('allEmpresasData/<int:organizacion_id>/', allEmpresasData, name='allEmpresasData'),
    path('allClientesData/<int:organizacion_id>/', allClientesData, name='allClientesData'),
    path('editcliente/<int:cliente_id>/', editcliente, name='editcliente'),
    path('listaClientes/<int:organizacion_id>/', listaClientes, name='listaClientes'),
    path('duplicarCotizacion/<int:cotizacion_id>/', duplicarCotizacion, name='duplicarCotizacion'),
    path('allcotizacionesdata/<int:organizacion_id>/', allcotizacionesdata, name='allcotizacionesdata'),
    path('detallecotizaciondata/<int:cotizacion_id>/', detalleCotizacionData, name='detallecotizaciondata'),
    path('crearOrdenTrabajo/<int:cotizacion_id>/', crearOrdenTrabajo, name='crearOrdenTrabajo'),
    path('crearFactura/<int:cotizacion_id>/', crearFactura, name='crearFactura'),
    path('allordentrabajodata/<int:organizacion_id>/', allOrdenTrabajoData, name='allordentrabajodata'),
    path('dataordentrabajo/<int:orden_id>/', dataOrdenTrabajo, name='dataordentrabajo'),
    path('dataordentrabajocrearfactura/<int:orden_id>/', dataOrdenTrabajoCrearFactura, name='dataordentrabajocrearfactura'),
    path('dataeditordentrabajo/<int:orden_id>/', dataEditOrdenTrabajo, name='dataeditordentrabajo'),
    path('allfacturasdata/<int:organizacion_id>/', allfacturasdata, name='allfacturasdata'),
    path('detallefacturadata/<int:factura_id>/', detalleFacturaData, name='detallefacturadata'),
    path('facturaCliente/<int:factura_id>/', facturaCliente, name='facturaCliente'),
    path('clienteFactura/<int:cliente_id>/', clienteFactura, name='clienteFactura'),
    path('facturaMontoTotal/<int:factura_id>/', facturaMontoTotal, name='facturaMontoTotal'),
    path('clienteConFactura/<int:organizacion_id>/', clienteConFactura, name='clienteConFactura'),
    path('allprecotizaciondata/<int:organizacion_id>/', allPrecotizacionData, name='allprecotizaciondata'),
    path('detalleprecotizaciondata/<int:precotizacion_id>/', detallePreCotizacionData, name='detalleprecotizaciondata'),
    path('allcomprobantepagodata/<int:organizacion_id>/', allcomprobantepagodata, name='allcomprobantepagodata'),
    path('contar_cotizaciones/', contar_cotizaciones, name='contar_cotizaciones'),
    path('direccionclienteempresa/<int:cliente_id>/', direccionclienteempresa, name='direccionclienteempresa'),
    path('factura/<int:factura_id>/pagos', pagosFactura, name='pagosFactura'),
    path('factura-data/<int:factura_id>/', get_factura_data, name='get_factura_data'),
    path('carga-csd/<int:organizacion_id>/', carga_csd, name='carga_csd'),
    path('borrar-csd/<int:organizacion_id>/', borrar_csd, name='borrar_csd'),
    path('factura-detail/<str:factura_id>/', factura_detail, name='factura_detail'),
    path('factura-delete/<str:factura_id>/', factura_delete, name='factura_delete'),
    path('factura-pdf/<str:factura_id>/', factura_pdf, name='factura_pdf'),
    path('factura-xml/<str:factura_id>/', factura_xml, name='factura_xml'),
    path('factura-pdf/<str:factura_id>/enviar', factura_pdf_enviar, name='factura_pdf_enviar'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cotizacion/<int:cotizacion_id>/pdf/', generar_pdf_cotizacion, name='generar_pdf_cotizacion'),
    path('ordentrabajo/<int:ordentrabajo_id>/pdf/', generar_pdf_orden_trabajo, name='generar_pdf_orden_trabajo'),
    path('cotizacion/<int:cotizacion_id>/pdf/enviar', enviar_pdf_cotizacion, name='enviar_pdf_cotizacion'),
    path('currency/', CurrencyView.as_view(), name='currency'),
    path('precotizacion/<int:precotizacion_id>/pdf/', generar_pdf_precotizacion, name='generar_pdf_precotizacion'),
    path('precotizacion/<int:precotizacion_id>/pdf/enviar', enviar_pdf_precotizacion, name='enviar_pdf_precotizacion'),
    path('complemento-pago/<int:comprobante_pago_id>/', get_complemento_pago, name='get_complemento_pago'),
    path('complemento-pdf/<int:comprobante_id>/', comprobante_pdf, name='comprobante_pdf'),
    path('comprobantepago/<int:comprobante_id>/enviar', comprobante_pdf_enviar, name='comprobante_pdf_enviar'),
    path('comprobante-delete/<int:comprobante_id>/', comprobante_delete, name='comprobante_delete'),
    path('allMetodosData/<int:organizacion_id>/', allMetodosData, name='allMetodosData'),
    path('allServiciosData/<int:organizacion_id>/', allServiciosData, name='allServiciosData'),
    path('obtener_csd/<int:organizacion_id>/', obtener_csd, name='obtener_csd'),
    path('pasarprecotizacion/<int:id>/', pasarprecotizacion, name='pasarprecotizacion'),
    path('comprobante-xml/<int:comprobante_id>/', comprobante_xml, name='comprobante_xml'),
]