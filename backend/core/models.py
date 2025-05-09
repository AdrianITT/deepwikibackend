from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models import Max, Count

class RegimenFiscal(models.Model):
    codigo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.codigo + ' - ' + self.nombre

class TipoMoneda(models.Model):
    codigo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion

class Iva(models.Model):
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.porcentaje}%"


class ImagenMarcaAgua(models.Model):
    imagen = models.ImageField(upload_to='marca_agua/')

    def __str__(self):
        return self.imagen.name


class Rol(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    organizacion = models.ForeignKey('Organizacion', on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return f"{self.username} ({self.rol})"


class Titulo(models.Model):
    titulo = models.CharField(max_length=255)
    abreviatura = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.titulo} ({self.abreviatura})"


class UnidadCfdi(models.Model):
    codigo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} {self.nombre}"

class ClaveCfdi(models.Model):
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class ObjetoImpuesto(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class UsoCfdi(models.Model):
    codigo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class FormaPago(models.Model):
    codigo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"
    
class MetodoPago(models.Model):
    codigo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}" 
    
class TipoCfdi(models.Model):
    codigo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"   

class Receptor(models.Model):
    nombrePila = models.CharField(max_length=255)
    apPaterno = models.CharField(max_length=255)
    apMaterno = models.CharField(max_length=255)
    correo = models.EmailField(blank=True, null=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    organizacion = models.ForeignKey('Organizacion', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombrePila} {self.apPaterno} {self.apMaterno}"

class InfoOrdenTrabajo(models.Model):
    nombreFormato = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    fechaEmision = models.DateField()
    tituloDocumento = models.CharField(max_length=255)
    imagenMarcaAgua = models.ForeignKey(ImagenMarcaAgua, on_delete=models.CASCADE)

    def __str__(self):
        return self.tituloDocumento

class InfoCotizacion(models.Model):
    nombreFormato = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    fechaEmision = models.DateField()
    tituloDocumento = models.CharField(max_length=255)
    mensajePropuesta = models.TextField()
    termino = models.TextField()
    avisos = models.TextField()
    imagenMarcaAgua = models.ForeignKey(ImagenMarcaAgua, on_delete=models.CASCADE)

    def __str__(self):
        return self.tituloDocumento

class InfoSistema(models.Model):
    tipoCambioDolar = models.DecimalField(max_digits=10, decimal_places=2)
    tipoMoneda = models.ForeignKey(TipoMoneda, on_delete=models.CASCADE)
    iva = models.ForeignKey(Iva, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tipo de Cambio: {self.tipoCambioDolar} - IVA: {self.iva.porcentaje}%"

class Organizacion(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    colonia = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    calle = models.CharField(max_length=255)
    codigoPostal = models.CharField(max_length=10)
    estado = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    pagina = models.URLField()
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    infoCotizacion = models.ForeignKey(InfoCotizacion, on_delete=models.CASCADE)
    infoOrdenTrabajo = models.ForeignKey(InfoOrdenTrabajo, on_delete=models.CASCADE)
    infoSistema = models.ForeignKey(InfoSistema, on_delete=models.CASCADE)
    RegimenFiscal = models.ForeignKey(RegimenFiscal, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre 

class Metodos(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    codigo = models.CharField(max_length=255)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Solo al crear, y si no se pasó número manualmente
        if self._state.adding and self.numero is None:
            ultimo = Metodos.objects.filter(organizacion=self.organizacion) \
                                  .aggregate(max_num=models.Max('numero'))['max_num']
            self.numero = (ultimo or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo
    
class CertificadoSelloDigital(models.Model):
    rfc = models.CharField(max_length=255)
    archivocer = models.FileField(upload_to='certificados/')
    archivokey = models.FileField(upload_to='certificados/')
    contrasenia = models.CharField(max_length=255)
    Organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Certificado Sello Digital - {self.rfc}"

class Empresa(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    nombre = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    codigoPostal = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    colonia = models.CharField(max_length=255)
    numeroExterior = models.CharField(max_length=10, null=True, blank=True)
    calle = models.CharField(max_length=255)
    UsoCfdi = models.ForeignKey(UsoCfdi, on_delete=models.CASCADE, null=True, blank=True)
    regimenFiscal = models.ForeignKey(RegimenFiscal, on_delete=models.CASCADE, null=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding and self.numero is None:
            ultimo = Empresa.objects.filter(organizacion=self.organizacion).aggregate(max_num=models.Max('numero'))['max_num']
            self.numero = (ultimo or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    nombrePila = models.CharField(max_length=255)
    apPaterno = models.CharField(max_length=255)
    apMaterno = models.CharField(max_length=255, null=True, blank=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    codigoPostalCliente = models.CharField(max_length=10, null=True, blank=True)
    ciudadCliente = models.CharField(max_length=255, null=True, blank=True)
    estadoCliente = models.CharField(max_length=255, null=True, blank=True)
    coloniaCliente = models.CharField(max_length=255, null=True, blank=True)
    numeroCliente = models.CharField(max_length=10, null=True, blank=True)
    calleCliente = models.CharField(max_length=255, null=True, blank=True)
    division = models.CharField(max_length=255, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding and self.numero is None:
            organizacion = self.empresa.organizacion
            ultimo = Cliente.objects.filter(empresa__organizacion=organizacion).aggregate(max_num=models.Max('numero'))['max_num']
            self.numero = (ultimo or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombrePila} {self.apPaterno} {self.apMaterno}"


class Servicio(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    nombreServicio = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    unidadCfdi = models.ForeignKey(UnidadCfdi, on_delete=models.CASCADE)
    metodos = models.ForeignKey(Metodos, on_delete=models.CASCADE)
    claveCfdi = models.ForeignKey(ClaveCfdi, on_delete=models.CASCADE)
    objetoImpuesto = models.ForeignKey(ObjetoImpuesto, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Solo asignar número si es un nuevo objeto
        if self._state.adding and self.numero is None:
            ultimo_numero = Servicio.objects.filter(organizacion=self.organizacion).aggregate(
                ultimo=models.Max('numero'))['ultimo']
            self.numero = (ultimo_numero or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organizacion.nombre} - {self.numero} - {self.nombreServicio} - ${self.precio}"

class Cotizacion(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    denominacion = models.CharField(max_length=255)
    fechaSolicitud = models.DateField()
    fechaCaducidad = models.DateField()
    descuento = models.IntegerField()
    iva = models.ForeignKey(Iva, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio, through='CotizacionServicio')
    tipoMoneda = models.ForeignKey(TipoMoneda, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding and self.numero is None:
            organizacion = self.cliente.empresa.organizacion
            ultimo = Cotizacion.objects.filter(cliente__empresa__organizacion=organizacion).aggregate(max_num=models.Max('numero'))['max_num']
            self.numero = (ultimo or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Id: {self.id} Cotización {self.numero} - {self.cliente.nombrePila} {self.cliente.apPaterno} {self.cliente.apMaterno}"


class CotizacionServicio(models.Model):
    descripcion = models.TextField(default="")
    precio= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
class PreCotizacion(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    nombreEmpresa = models.CharField(max_length=255)
    nombreCliente = models.CharField(max_length=255)
    apellidoCliente = models.CharField(max_length=255)
    correo = models.EmailField()
    denominacion = models.CharField(max_length=255)
    fechaSolicitud = models.DateField()
    fechaCaducidad = models.DateField()
    descuento = models.IntegerField()
    iva = models.ForeignKey(Iva, on_delete=models.CASCADE)
    tipoMoneda = models.ForeignKey(TipoMoneda, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    servicio = models.ManyToManyField(Servicio, through='PreCotizacionServicio')
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding and self.numero is None:
            ultimo = PreCotizacion.objects.filter(organizacion=self.organizacion).aggregate(max_num=models.Max('numero'))['max_num']
            self.numero = (ultimo or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pre-Cotización {self.numero} de {self.nombreEmpresa} - {self.nombreCliente} {self.apellidoCliente}"

class PreCotizacionServicio(models.Model):
    descripcion = models.TextField(default="")
    precio= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preCotizacion = models.ForeignKey(PreCotizacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.cantidad} x {self.servicio.nombreServicio} en Pre-Cotizacion {self.preCotizacion.id}"
    
    
class OrdenTrabajo(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    codigo = models.CharField(max_length=255, blank=True)
    estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
    receptor = models.ForeignKey('Receptor', on_delete=models.CASCADE)
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE)
    servicio = models.ManyToManyField('Servicio', through='OrdenTrabajoServicio')

    def save(self, *args, **kwargs):
        # Sólo al crear una nueva orden...
        if self._state.adding:
            # 1) Determina la organización
            org = self.cotizacion.cliente.empresa.organizacion

            # 2) Asigna numero secuencial por organización (no se reinicia)
            if self.numero is None:
                last_num = OrdenTrabajo.objects.filter(
                    cotizacion__cliente__empresa__organizacion=org
                ).aggregate(max_num=Max('numero'))['max_num']
                self.numero = (last_num or 0) + 1

            # 3) Genera el código diario por organización (reinicia a 01 cada día)
            today = now().strftime('%y%m%d')  # e.g. "250425"
            # Cuenta cuántas órdenes ya hay hoy para esta organización
            count_today = OrdenTrabajo.objects.filter(
                codigo__startswith=today,
                cotizacion__cliente__empresa__organizacion=org
            ).count()
            new_idx = count_today + 1
            self.codigo = f"{today}-{new_idx:02d}"  # e.g. "250425-01", "250425-02", etc.

        super().save(*args, **kwargs)

    def __str__(self):
        return f"OT {self.numero} – {self.codigo}"

class OrdenTrabajoServicio(models.Model):
    ordenTrabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.cantidad} x {self.servicio.nombreServicio} en Orden {self.ordenTrabajo.id}"
  

class Factura(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    ordenCompra = models.CharField(null=True, blank=True, max_length=255)
    fechaExpedicion = models.DateTimeField()
    tipoCfdi = models.ForeignKey(TipoCfdi, on_delete=models.CASCADE)
    formaPago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    metodoPago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    porcentaje = models.IntegerField(null=True, blank=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipoMoneda = models.TextField(max_length=255, blank=True, null=True)
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.ManyToManyField('Servicio', through='FacturaServicio')

    def save(self, *args, **kwargs):
        if self._state.adding and self.numero is None and self.cotizacion:
            # Obtener la organización a través de cotización → cliente → empresa → organización
            organizacion = self.cotizacion.cliente.empresa.organizacion
            ultimo = Factura.objects.filter(
                cotizacion__cliente__empresa__organizacion=organizacion
            ).aggregate(max_num=models.Max('numero'))['max_num']
            self.numero = (ultimo or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        num = self.numero if self.numero is not None else self.id
        return f"Factura {num} - Cotización {self.cotizacion.numero if self.cotizacion else 'N/A'} - {self.fechaExpedicion:%Y-%m-%d}"

class FacturaServicio(models.Model):
    descripcion = models.TextField(default="")
    precio= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.cantidad} x {self.servicio.nombreServicio} en Factura {self.factura.id}"
                                                    
class FacturaFacturama(models.Model):
    #id
    uuid = models.TextField()
    idfactura = models.TextField()
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura {self.uuid}"
    
class ComprobantePago(models.Model):
    numero = models.PositiveIntegerField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fechaPago = models.DateTimeField()
    formapago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    factura = models.ManyToManyField(Factura, through='ComprobantePagoFactura')
    facturama_id = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Comprobante de Pago {self.id} Fecha de Pago {self.fechaPago}"
    
class ComprobantePagoFactura(models.Model):
    comprobantepago = models.ForeignKey(ComprobantePago, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    montototal = models.DecimalField(max_digits=10, decimal_places=2)
    montorestante = models.DecimalField(max_digits=10, decimal_places=2)
    montopago = models.DecimalField(max_digits=10, decimal_places=2)
    parcialidad = models.PositiveIntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self._state.adding and self.comprobantepago.numero is None:
            factura = self.factura
            organizacion = factura.cotizacion.cliente.empresa.organizacion
            ultimo_numero = ComprobantePago.objects.filter(
                factura__cotizacion__cliente__empresa__organizacion=organizacion
            ).aggregate(models.Max('numero'))['numero__max']
            self.comprobantepago.numero = (ultimo_numero or 0) + 1
            self.comprobantepago.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Comprobante de Pago {self.comprobantepago.id} - {self.factura.id} por {self.montopago}"

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max

@receiver(post_save, sender=ComprobantePagoFactura)
def asignar_numero_comprobante(sender, instance, created, **kwargs):
    if not created:
        return

    cp = instance.comprobantepago
    if cp.numero is not None:
        return

    # Navegamos la relación para sacar la organización
    organizacion = (
        instance.factura
                .cotizacion
                .cliente
                .empresa
                .organizacion
    )

    ultimo = ComprobantePago.objects.filter(
        factura__cotizacion__cliente__empresa__organizacion=organizacion
    ).aggregate(max_num=Max('numero'))['max_num']

    cp.numero = (ultimo or 0) + 1
    cp.save(update_fields=['numero'])
