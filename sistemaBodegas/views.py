from django.shortcuts import render

def login(request):
    return render(request, 'static/login.html')

def home(request):
    return render(request, 'static/index.html')

def productos(request):
    return render(request, 'static/productos.html',{'navbar':'productos'})

def nuevoProducto(request):
    return render(request, 'static/guardar.html',{'navbar':'productos'})

def buscar(request):
    return render(request, 'static/busqueda.html',{'navbar':'buscar'})

def inventario(request):
    return render(request, 'static/inventario.html',{'navbar':'inventario'})

def buscarInvent(request,id,cod_prod, talla):
    return render(request, 'static/resultado.html',{'navbar':'buscar'})

def editar(request,id):
    return render(request, 'static/editar.html')

def cuerpoReporte(request):
    return render(request, 'static/cuerporeporte.html')

def bodega(request):
    return render(request, 'static/bodegas.html')

def reporteTalla(request):
    return render(request, 'static/reportetalla.html')

def reporte(request):
    return render(request, 'static/reporte.html',{'navbar':'reporte'})