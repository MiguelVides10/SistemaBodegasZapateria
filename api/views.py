from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import Categorias,Productos,Marcas,Bodegas,ProductosBodegas,Proveedores
from .serializers import CategoriasSerializer,ProductosSerializer,MarcasSerializer,BodegasSerializer,ProductosBodegasSerializer,ProveedoresSerializer

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

def check_token(request):
    return Response({"message": "Token válido"})

class EliminarToken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        
        token.delete()
        
        return Response({"sucess":True,"mensaje": "Token eliminado correctamente"})

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class ListaCategorias(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        categorias = Categorias.objects.all()
        serializer = CategoriasSerializer(categorias, many=True)

        if categorias.exists():
            response_data = {
                "success": True,
                "data": serializer.data
            }
        else:
            response_data = {
                "success": False,
                "data": []
            }
        return Response(response_data)

class ListaBodegas(APIView):
    def get(self, request, *args, **kwargs):
        bodegas = Bodegas.objects.all()
        serializer = BodegasSerializer(bodegas, many=True)

        if bodegas.exists():
            response_data = {
                "success": True,
                "data": serializer.data
            }
        else:
            response_data = {
                "success": False,
                "data": []
            }

        return Response(response_data)
    
class ListaMarcas(APIView):
    def get(self, request, *args, **kwargs):
        marcas = Marcas.objects.all()
        serializer = MarcasSerializer(marcas, many=True)
        if marcas.exists():
            response_data = {
                "success": True,
                "data": serializer.data
            }
        else:
            response_data = {
                "success": False,
                "data": []
            }
        return Response(response_data)

class ListaProveedores(APIView):
    def get(self, request, *args, **kwargs):
        proveedores = Proveedores.objects.all()
        serializer = ProveedoresSerializer(proveedores, many=True)
        if proveedores.exists():
            response_data = {
                "success": True,
                "data": serializer.data
            }
        else:
            response_data = {
                "success": False,
                "data": []
            }
        return Response(response_data)
    
class ProductoConMarcaListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("Select cod_prod,descripcion,nombre_marca as marca,categoria,color,precio from productos inner join marcas using(id_marca) inner join categorias using(id_categoria)")
            rows = dictfetchall(cursor)

        response_data = {
            "success": True,
            "data": rows
        }
        return Response(response_data)
    
class ListaProductos(APIView):
    def get(self, request, *args, **kwargs):
        productos = Productos.objects.all()
        serializer = ProductosSerializer(productos, many=True)
        if productos.exists():
            response_data = {
                "success": True,
                "data": serializer.data
            }
        else:
            response_data = {
                "success": False,
                "data": []
            }
        return Response(response_data)
    
class ProductosCreateView(generics.CreateAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True, "message": "Producto creado correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "No se pudo crear el producto", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class InventarioCreateView(generics.CreateAPIView):
    queryset = ProductosBodegas.objects.all()
    serializer_class = ProductosBodegasSerializer
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            num_fact = request.POST.getlist('numfac')
            fecha = request.POST.getlist('fecha')
            id_proveedor = request.POST.getlist('id_proveedor')
            descuento = request.POST.getlist('descuento')
            total = request.POST.getlist('total')
            totalDesc = request.POST.getlist('totalDesc')
            consulta = 'INSERT into facturas set num_fact = %s,descuento = %s, cod_proveedor = %s, total=%s, totalDesc = %s'
            parametros = (num_fact,descuento,id_proveedor,total,totalDesc)
            with connection.cursor() as cursor:
                cursor.execute(consulta, parametros)

            bodegas = request.POST.getlist('bodegas[]')
            productos = request.POST.getlist('productos[]')
            tallas = request.POST.getlist('tallas[]')
            cantidades = request.POST.getlist('cantidades[]')
            costos = request.POST.getlist('costos[]')
            totales = request.POST.getlist('totales[]')
            for index, item in enumerate(productos):
                consulta = "INSERT INTO sistema_bodegas.productos_bodegas (id_sucursal, cod_prod, talla, cantidad,costo,total,tipo) VALUES(%s, %s, %s, %s, %s, %s, 'carga')"
                parametros = (bodegas[index],item,tallas[index],cantidades[index],costos[index],totales[index])
                with connection.cursor() as cursor:
                    cursor.execute(consulta, parametros)
            return Response({"success": True, "message": "Registros insertados"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"success": False, "message": "Bad request"})



class MarcasCreateView(generics.CreateAPIView):
    queryset = Marcas.objects.all()
    serializer_class = MarcasSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True, "message": "Marca creada correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "No se pudo crear la Marca", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProveedoresCreateView(generics.CreateAPIView):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedoresSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True, "message": "Proveedor creado correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "No se pudo crear el proveedor", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CategoriasCreateView(generics.CreateAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriasSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True, "message": "Categoria creada correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "No se pudo crear la Categoria", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductoId(APIView):
    def get(self, request, id, *args, **kwargs):
        productos = list(Productos.objects.filter(cod_prod=id).values())
        if(len(productos)>0):
            producto= productos[0]
        serializer = ProductosSerializer(producto, many=False)

        response_data = {
            "success": True,
            "data": serializer.data
        }
        return Response(response_data)
    
class ProductoDelete (generics.DestroyAPIView):
    queryset= Productos.objects.all()
    serializer_class = ProductosSerializer
    lookup_field = 'cod_prod'
    def delete(self, request, *args, **kargs):
       instance = self.get_object()
       serializer = self.get_serializer(instance, data = request.data, partial= True)
       if serializer.is_valid():
           instance.delete()
           return Response({"success": True, "message": "Producto Eliminado correctamente"})
       else :
           return Response({"success": False, "message": "No se pudo actualizar el producto", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  


class ProductoUpdateApiView(generics.UpdateAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer
    lookup_field = 'cod_prod'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Producto actualizado correctamente"})
        else:
            return Response({"success": False, "message": "No se pudo actualizar el producto", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  



class InventarioConDatosListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        cod_prod = request.query_params.get('cod_prod', "")
        talla = request.query_params.get('talla', 0)
        bodega = request.query_params.get('id_sucursal', 0)

        with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(CASE WHEN tipo = 'carga' THEN total ELSE 0 END) - SUM(CASE WHEN tipo = 'descarga' THEN total ELSE 0 END) AS total, p.descripcion as nombre, p.color, b.nom_sucursal as bodega,b.id_sucursal,p.cod_prod, pb.talla, p.precio, m.nombre_marca as marca, p.foto FROM productos p INNER JOIN marcas m ON p.id_marca = m.id_marca INNER JOIN productos_bodegas pb ON p.cod_prod = pb.cod_prod INNER JOIN bodegas b ON pb.id_sucursal = b.id_sucursal WHERE p.cod_prod = %s AND pb.talla = %s AND b.id_sucursal = %s GROUP BY p.descripcion,p.precio ,p.cod_prod,p.color, b.id_sucursal, pb.talla,m.nombre_marca,p.foto",
                    [cod_prod, talla, bodega])
            rows = dictfetchall(cursor)

        response_data = {
            "success": True,
            "data": rows,
        }
        return Response(response_data)

class InventarioReporteListView (generics.ListAPIView):
    def get(self, request, *args, **kwargs):

        with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(CASE WHEN tipo = 'carga' THEN total ELSE 0 END) - SUM(CASE WHEN tipo = 'descarga' THEN total ELSE 0 END) AS total,p.descripcion as nombre,m.nombre_marca as marca, p.color, pb.talla, p.precio, b.nom_sucursal as bodega, b.direccion as direccion FROM productos p INNER JOIN marcas m using(id_marca)  INNER JOIN productos_bodegas pb using(cod_prod) INNER JOIN bodegas b using(id_sucursal) GROUP BY p.cod_prod, b.id_sucursal, pb.talla,p.descripcion,m.nombre_marca,p.color,p.precio")
            rows = dictfetchall(cursor)

        response_data = {
            "success": True,
            "data": rows,
        }
        return Response(response_data)
    
class InventarioReporteTallaListView(generics.ListAPIView):
    
    def get(self, request, *args, **kwargs):
        cod_prod= request.query_params.get('cod_prod',"")
        with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(CASE WHEN tipo = 'carga' THEN total ELSE 0 END) - SUM(CASE WHEN tipo = 'descarga' THEN total ELSE 0 END) AS total,p.descripcion as nombre,m.nombre_marca as marca, p.color, pb.talla, p.precio, b.nom_sucursal as bodega, b.direccion as direccion FROM productos p INNER JOIN marcas m using(id_marca)  INNER JOIN productos_bodegas pb using(cod_prod) INNER JOIN bodegas b using(id_sucursal) WHERE p.cod_prod =%s GROUP BY p.cod_prod, b.id_sucursal, pb.talla,p.descripcion,m.nombre_marca,p.color,p.precio",[cod_prod])
            rows = dictfetchall(cursor)

        response_data = {
            "success": True,
            "data": rows,
        }
        return Response(response_data)
    
class VenderProductoView(generics.CreateAPIView):
    queryset = ProductosBodegas.objects.all()
    serializer_class = ProductosBodegasSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"success": True, "message": "Venta realizada correctamente"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "No se pudo crear la Marca", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
