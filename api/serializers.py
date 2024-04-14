from rest_framework import serializers
from .models import Bodegas,Categorias,Productos,ProductosBodegas,Marcas

class BodegasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodegas
        fields = '__all__'

class CategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'

class MarcasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marcas
        fields = '__all__'
class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'
        def create(self, validated_data):
            producto = Productos.objects.create(**validated_data)
            return producto

class ProductosBodegasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductosBodegas
        fields = '__all__'
        def create(self, validated_data):
            producto = Productos.objects.create(**validated_data)
            return producto
