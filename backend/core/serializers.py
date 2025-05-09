from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import RegimenFiscal, TipoMoneda, Iva, ImagenMarcaAgua, Rol 
from .models import Titulo, UnidadCfdi, Metodos, ClaveCfdi, ObjetoImpuesto
from .models import Estado, Receptor, InfoOrdenTrabajo, InfoCotizacion
from .models import InfoSistema, Organizacion, Empresa, Cliente, Servicio
from .models import Cotizacion, OrdenTrabajo, Factura
from .models import CertificadoSelloDigital, FacturaFacturama
from .models import CotizacionServicio, User, OrdenTrabajoServicio
from .models import TipoCfdi, FormaPago, MetodoPago, UsoCfdi
from .models import PreCotizacion,PreCotizacionServicio, ComprobantePago
from .models import ComprobantePagoFactura, FacturaServicio

class RegimenFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegimenFiscal
        fields = '__all__'

class TipoMonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMoneda
        fields = '__all__'
        
class IvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iva
        fields = '__all__'

class ImagenMarcaAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenMarcaAgua
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'password', 'organizacion']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hashea la contraseña antes de guardar el usuario
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Si se proporciona una nueva contraseña, se cifra antes de actualizar el usuario
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
        
class TituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titulo
        fields = '__all__'

class UnidadCfdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadCfdi
        fields = '__all__'
        
class MetodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodos
        fields = '__all__'

class ClaveCfdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaveCfdi
        fields = '__all__'

class ObjetoImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjetoImpuesto
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class TipoCfdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCfdi
        fields = '__all__'

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = '__all__'

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class UsoCfdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsoCfdi
        fields = '__all__'

class ReceptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptor
        fields = '__all__'

class InfoOrdenTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoOrdenTrabajo
        fields = '__all__'

class InfoCotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoCotizacion
        fields = '__all__'

class InfoSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoSistema
        fields = '__all__'

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class CotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotizacion
        fields = '__all__'

class CotizacionServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CotizacionServicio
        fields = '__all__'
        
class PreCotizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreCotizacion
        fields = '__all__'
        
class PreCotizacionServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreCotizacionServicio
        fields = '__all__'

class OrdenTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenTrabajo
        fields = '__all__'
        
class OrdenTrabajoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenTrabajoServicio
        fields = '__all__'

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
        
class FacturaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaServicio
        fields = '__all__'

class CertificadoSelloDigitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoSelloDigital
        fields = '__all__'

class FacturaFacturamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaFacturama
        fields = '__all__'
        
class ComprobantePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobantePago
        fields = '__all__'
        
class ComprobantePagoFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobantePagoFactura
        fields = '__all__'

