from django.contrib import admin
from .models import RegimenFiscal, TipoMoneda, Iva, ImagenMarcaAgua, Rol 
from .models import Titulo, UnidadCfdi, Metodos, ClaveCfdi, ObjetoImpuesto
from .models import Estado, Receptor, InfoOrdenTrabajo, InfoCotizacion
from .models import InfoSistema, Organizacion, Empresa, Cliente, Servicio
from .models import Cotizacion, OrdenTrabajo, Factura, User

admin.site.register(User)
admin.site.register(RegimenFiscal)
admin.site.register(TipoMoneda)
admin.site.register(Iva)
admin.site.register(ImagenMarcaAgua)
admin.site.register(Rol)
admin.site.register(Titulo)
admin.site.register(UnidadCfdi)
admin.site.register(Metodos)
admin.site.register(ClaveCfdi)
admin.site.register(ObjetoImpuesto)
admin.site.register(Estado)
admin.site.register(Receptor)
admin.site.register(InfoOrdenTrabajo)
admin.site.register(InfoCotizacion)
admin.site.register(InfoSistema)
admin.site.register(Organizacion)
admin.site.register(Empresa)
admin.site.register(Cliente)
admin.site.register(Servicio)
admin.site.register(Cotizacion)
admin.site.register(OrdenTrabajo)
admin.site.register(Factura)
  