from rest_framework import serializers
from cpmAPI.models import Test, Trabajador, Cliente, Obra, Avance, Material, InventarioObra


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('TestId',
                  'TestName')

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ('trabajador_id',
                  'numero_cedula',
                  'nombre',
                  'apellido',
                  'numero_celular',
                  'contrasena',
                  'cargo',
                  'is_active',
                  'obra_participante')

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('cliente_id',
                  'numero_nit',
                  'nombre',
                  'apellido',
                  'correo',
                  'direccion',
                  'contrasena',
                  'cargo',
                  'is_active')

class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = ('obra_id',
                  'nombre',
                  'direccion',
                  'ciudad',
                  'fase',
                  'latitud',
                  'longitud',
                  'cliente')


class AvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avance
        fields = ('avance_id',
                  'obra',
                  'descripcion',
                  'link',
                  'latitud',
                  'longitud',
                  'tipo',
                  'fecha',
                  'fase',
                  'aprobado',
                  'trabajador')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('material_id',
                  'nombre',
                  'cantidad',
                  'estado')


class InventarioObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioObra
        fields = ('obra',
                  'material',
                  'cantidad',
                  'aprobado')