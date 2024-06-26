from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from api import urls as api_urls
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('guardar/', views.nuevoProducto, name='guardar'),
    path('productos/', views.productos, name='productos'),
    path('buscar/',views.buscar, name='buscar'),
    path('inventario/',views.inventario, name='inventario'),
    path('reporte/',views.reporte,  name='reporte'),
    path('editar/<str:id>/',views.editar, name='editar'),
    path('buscar/<int:id>/<str:cod_prod>/<slug:talla>', views.buscarInvent, name="busqueda"),
    path('cuerpo/',views.cuerpoReporte, name='datos-reporte'),
    path('reporteportalla/', views.reporteTalla, name='reporte-talla'),
    path('reporteporcompras/', views.reporteCompras, name='reporte-talla'),
    path('reporteporcomprasProv/', views.reporteComprasProv, name='reporte-talla'),
    path('reporteporcomprasNum/', views.reporteComprasNum, name='reporte-talla'),
    path('reporteventasd/', views.reporteVentasd, name='reporte-ventasd'),
    path('reporteventasf/', views.reporteVentasf, name='reporte-ventasd'),
    path('bodegas/',views.bodega, name= 'bodegas'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include(api_urls)),
]


