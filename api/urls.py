# todo/todo/urls.py : Main urls.py
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('check-token/', check_token, name='check-token'),
    path('eliminar-token/', EliminarToken.as_view(), name='eliminar_token'),
    path('bodegas/', ListaBodegas.as_view(), name='lista-bodegas'),
    path('bodegas/<int:id>',BodegaId.as_view(), name='bodega-id'),
    path('editarBodega/<int:id_sucursal>', BodegaUpdateApiView.as_view(), name='bodega-edit'),
    path('eliminarBodega/<int:id_sucursal>', BodegaDelete.as_view(),name='bodega-delete'),
    path('categorias/', ListaCategorias.as_view(), name='lista-categorias'),
    path('marcas/', ListaMarcas.as_view(), name='lista-marcas'),
    path('proveedores/', ListaProveedores.as_view(), name='lista-proveedores'),
    path('productos/', ProductoConMarcaListView.as_view(), name='lista-productos'),
    path('guardarProducto/', ProductosCreateView.as_view(), name='create-item'),
    path('guardarInventario/', InventarioCreateView.as_view(), name='create-inventario'),
    path('venderInventario/', VenderProductoView.as_view(), name='vender-inventario'),
    path('guardarMarca/', MarcasCreateView.as_view(), name='create-marca'),
    path('guardarProveedor/', ProveedoresCreateView.as_view(), name='create-proveedor'),
    path('guardarBodega/', BodegasCreateView.as_view(), name='create-bodega'),
    path('guardarCategoria/', CategoriasCreateView.as_view(), name='create-categorias'),
    path('productos/<str:id>', ProductoId.as_view(), name='producto'),
    path('editarProducto/<str:cod_prod>', ProductoUpdateApiView.as_view(), name='producto-edit'),
    path('cuerpoReporte/',InventarioReporteListView.as_view(), name='reporte-productos'),
    path('cuerporeporteTalla/', InventarioReporteTallaListView.as_view(), name='repote-talla'),
    path('cuerporeporteCompras/', InventarioReporteComprasListView.as_view(), name='repote-talla'),
    path('eliminarProd/<str:cod_prod>',ProductoDelete.as_view(), name='delete-prod'),
    path('buscar/', InventarioConDatosListView.as_view(), name="datos"),
]
