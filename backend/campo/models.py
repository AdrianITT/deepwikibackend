from django.db import models
from core.models import OrdenTrabajo, Receptor

class Preservador(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Matriz(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.codigo + ' - ' + self.nombre

class Clave(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.codigo + ' - ' + self.nombre

class Contenedor(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.codigo + ' - ' + self.nombre
class Parametro(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Prioridad(models.Model):
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion\
            
#agregar tabla para idfiltro
class Filtro(models.Model):
    codigo = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.codigo + ' - ' + self.descripcion

class EstadoCustodia(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion

class CustodiaExterna(models.Model):
    contacto = models.CharField(max_length=50)
    puestoCargoContacto = models.CharField(max_length=50, null=True, blank=True)
    celularContacto = models.CharField(max_length=50, null=True, blank=True)
    correoContacto = models.EmailField(max_length=50, null=True, blank=True)
    puntosMuestreoAutorizados = models.CharField(max_length=50)
    modificacionOrdenTrabajo = models.BooleanField()
    observacionesModificacion = models.TextField(max_length=120, null=True, blank=True)
    asesoriaGestionAmbiental = models.BooleanField()
    muestreoRequerido = models.CharField(max_length=50)
    fechaFinal = models.DateField(null=True, blank=True)
    horaFinal = models.TimeField(null=True, blank=True)
    muestraCompuesta = models.BooleanField()
    idMuestraCompuesta = models.CharField(max_length=50, null=True, blank=True)
    muestraPuntual = models.BooleanField()
    idMuestraPuntual = models.CharField(max_length=50, null=True, blank=True)
    observaciones = models.TextField(max_length=325, null=True, blank=True)
    estado = models.ForeignKey(EstadoCustodia, on_delete=models.CASCADE)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.CASCADE)
    #receptor solo se elegira uno pero en el excel deberan ir 3
    #(elegido), Israel, Humberto
    receptor = models.ForeignKey(Receptor, on_delete=models.CASCADE)
    ordenTrabajo = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE)

    def __str__(self):
        return f"CustodiaExterna - {self.contacto}"

class Muestra(models.Model):
    #nomenclaruta de la identificacion de campo
    #nomenclatura-filtro-corrida-contenedor-numero de ducto
    identificacionCampo = models.CharField(max_length=50)
    fechaMuestreo = models.DateField()
    horaMuestreo = models.TimeField()
    volumenCantidad = models.CharField(max_length=50, null=True, blank=True)
    numeroContenedor = models.CharField(max_length=50)
    origenMuestra = models.CharField(max_length=50)
    idLaboratorio = models.CharField(max_length=50, null=True, blank=True)
    filtro = models.ForeignKey(Filtro, on_delete=models.CASCADE, null=True, blank=True)
    preservador = models.ManyToManyField(Preservador, through='PreservadorMuestra')
    matriz = models.ForeignKey(Matriz, on_delete=models.CASCADE)
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE)
    parametro = models.ForeignKey(Parametro, on_delete=models.CASCADE)
    custodiaExterna = models.ForeignKey(CustodiaExterna, on_delete=models.CASCADE)

    def __str__(self):
        return f"Muestra - {self.identificacionCampo}"
    
class PreservadorMuestra(models.Model):
    preservador = models.ForeignKey(Preservador, on_delete=models.CASCADE)
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"PreservadorMuestra - {self.preservador} - {self.muestra}"

#mover a la app del laboratorio
class RegistroCustodia(models.Model):
    CustodiaExterna = models.ForeignKey(CustodiaExterna, on_delete=models.CASCADE)
    entregadoPor = models.CharField(max_length=100)
    fechaEntrega = models.DateField()
    horaEntrega = models.TimeField()
    recibidoPor = models.CharField(max_length=100)
    fechaEecepcion = models.DateField()
    horaRecepcion = models.TimeField()

    def __str__(self):
        return f"Registro de Custodia - Entregado por {self.entregadoPor} a {self.recibidoPor}"

