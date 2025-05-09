from rest_framework import serializers
from .models import Preservador, Matriz, Clave, Contenedor, Parametro, Prioridad, CustodiaExterna, Muestra
from .models import RegistroCustodia, Filtro, PreservadorMuestra, EstadoCustodia

class PreservadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preservador
        fields = '__all__'
        
class MatrizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matriz
        fields = '__all__'
        
class ClaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clave
        fields = '__all__'
        
class ContenedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenedor
        fields = '__all__'
        
class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = '__all__'
        
class PrioridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridad
        fields = '__all__'
        
class EstadoCustodiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCustodia
        fields = '__all__'
        
class CustodiaExternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustodiaExterna
        fields = '__all__'
        
class MuestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muestra
        fields = '__all__'
        
class RegistroCustodiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroCustodia
        fields = '__all__'
        
class FiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filtro
        fields = '__all__'
        
class PreservadorMuestraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreservadorMuestra
        fields = '__all__'