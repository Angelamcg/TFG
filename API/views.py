from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.defaultfilters import linebreaksbr
from django.db.models import Sum, F
from calendar import monthrange


from .models import Devolucion, FilaDevolucion, Proveedor, Cliente, Producto, Compra, Almacen, Plano, Venta, FilaVenta
from django.contrib.auth.models import User


def mostrarIndex(request):
    queryset = request.GET.get("buscar")
    order_by = request.GET.get('order_by')
    tipo_seleccionado = request.GET.get('tipo')

    prod = Producto.objects.all()

    if queryset:
        prod = prod.filter(
            Q(nombre__icontains=queryset) |
            Q(referencia__icontains=queryset) |
            Q(descripcion__icontains=queryset) |
            Q(id_proveedor__nombre_empresa__icontains=queryset)
        ).distinct()

    if tipo_seleccionado:
        prod = prod.filter(tipo=tipo_seleccionado)

    if order_by == 'nombre_asc':
        prod = prod.order_by('nombre')
    elif order_by == 'nombre_desc':
        prod = prod.order_by('-nombre')
    elif order_by == 'cantidad_asc':
        prod = prod.order_by('cantidad')
    elif order_by == 'cantidad_desc':
        prod = prod.order_by('-cantidad')
    elif order_by == 'referencia_asc':
        prod = prod.order_by('referencia')
    elif order_by == 'referencia_desc':
        prod = prod.order_by('-referencia')

    # Paginación
    paginator = Paginator(prod, 4)
    current_page = request.GET.get('page', 1)
    prod_page = paginator.get_page(current_page)

    tipos_producto = ["", "techo", "aplique", "plafon",
                      "flexos", "pie", "infantil", "exterior", "ventiladores"]

    datos = {
        'prod': prod_page,
        'tipos_producto': tipos_producto,
        'tipo_seleccionado': tipo_seleccionado,
    }

    return render(request, 'index.html', datos)


# ---------------------------------------------------------------------------------------
# PROVEEDORES

def mostrarListadoProv(request):
    queryset = request.GET.get("buscar")
    if queryset:
        prov = Proveedor.objects.filter(
            Q(nombre_empresa__icontains=queryset) |
            Q(cif__icontains=queryset) |
            Q(email__icontains=queryset) |
            Q(telefono__icontains=queryset) |
            Q(web__icontains=queryset)
        ).distinct()
    else:
        prov = Proveedor.objects.all().values()

    # Paginación
    paginator = Paginator(prov, 10)
    current_page = request.GET.get('page', 1)
    prov_page = paginator.get_page(current_page)

    datos = {'prov': prov_page}

    return render(request, 'proveedores/listado_prov.html', datos)


def mostrarFormRegistrarProv(request):
    return render(request, 'proveedores/form_registrar_prov.html')


def insertarProv(request):
    if request.method == 'POST':  
        nom = request.POST['txtnom']
        cif = request.POST['txtcif']
        email = request.POST['txtemail']
        telefono = request.POST['txttel']
        web = request.POST['txtweb']
        prov = Proveedor(nombre_empresa=nom, cif=cif,
                         email=email, telefono=telefono, web=web)
        try:
            prov.save()
            datos = {
                'r': '¡Datos insertados correctamente del proveedor: '+str(nom)+'!'}
            return render(request, 'proveedores/form_registrar_prov.html', datos)

        except IntegrityError:
            datos = {'r2': "ERROR: El CIF ya está registrado"}
            return render(request, 'proveedores/form_registrar_prov.html', datos)

    else:
        # r2 variable que indica error
        datos = {'r2': "ERROR: No se puede insertar proveedor"}
        return render(request, 'proveedores/form_registrar_prov.html', datos)


def mostrarFormActualizarProv(request, id):
    try:
        prov = Proveedor.objects.get(id=id)
        datos = {'prov': prov}
        return render(request, 'proveedores/form_actualizar_prov.html', datos)

    except ObjectDoesNotExist:
        prov = Proveedor.objects.all().values()
        datos = {'prov': prov,
                 'r2': 'El proveedor con ID ('+str(id)+') no existe.'
                 }
        return render(request, 'proveedores/listado_prov.html', datos)


def actualizarProv(request, id):
    try:
        prov = get_object_or_404(Proveedor, id=id)
    except ObjectDoesNotExist:
        datos = {'r2': 'No se puede encontrar el proveedor.'}
        return render(request, 'proveedores/listado_prov.html', datos)

    if request.method == 'POST':
        nom = request.POST['txtnom']
        cif = request.POST['txtcif']
        email = request.POST['txtemail']
        telefono = request.POST['txttel']
        web = request.POST['txtweb']

        # Comprueba que no haya otro proveedor con el mismo CIF
        proveedor_existente = Proveedor.objects.exclude(id=id).filter(cif=cif)

        if proveedor_existente:
            datos = {
                'r2': 'Ya existe el proveedor '+str(nom)+' con el CIF: '+str(cif)
            }
            return render(request, 'proveedores/listado_prov.html', datos)

        prov.nombre_empresa = nom
        prov.cif = cif
        prov.email = email
        prov.telefono = telefono
        prov.web = web
        prov.save()
        prov = Proveedor.objects.all().values()
        datos = {
            'prov': prov,
            'r': 'Datos modificados correctamente del proveedor: '+str(nom)
        }
        return render(request, 'proveedores/listado_prov.html', datos)
    else:
        datos = {'r2': 'No se puede actualizar el proveedor'}
        return render(request, 'proveedores/listado_prov.html', datos)


def eliminarProv(request, id):
    try:
        prov = Proveedor.objects.get(id=id)
    except ObjectDoesNotExist:
        datos = {'r2': 'No se puede encontrar el proveedor'}
        return render(request, 'proveedores/listado_prov.html', datos)

    if request.method == 'POST':
        nom = prov.nombre_empresa
        prov.delete()
        messages.success(
            request, '¡El proveedor {} ha sido eliminado correctamente!'.format(nom))
        return redirect('mostrarListadoProv')
        # datos = {'r': 'El proveedor ' +
        #          str(nom)+' ha sido eliminado correctamente'}
        # return render(request, 'proveedores/listado_prov.html', datos)

    datos = {'prov': prov}

    # Se muestra un formulario de confirmación
    return render(request, 'proveedores/form_eliminar_prov.html', datos)


# ---------------------------------------------------------------------------------------
# CLIENTES


def mostrarListadoCl(request):
    queryset = request.GET.get("buscar")
    if queryset:
        cl = Cliente.objects.filter(
            Q(nombre_empresa__icontains=queryset) |
            Q(cif__icontains=queryset) |
            Q(email__icontains=queryset) |
            Q(telefono__icontains=queryset) |
            Q(web__icontains=queryset)
        ).distinct()
    else:
        cl = Cliente.objects.all().values()

    # Paginación
    paginator = Paginator(cl, 10)
    current_page = request.GET.get('page', 1)
    cl_page = paginator.get_page(current_page)

    datos = {'cl': cl_page}
    # datos = {'cl': cl}
    return render(request, 'clientes/listado_cl.html', datos)


def mostrarFormRegistrarCl(request):
    return render(request, 'clientes/form_registrar_cl.html')


def insertarCl(request):
    if request.method == 'POST':  # si se ha pulsado el boton de insertar
        nom = request.POST['txtnom']
        cif = request.POST['txtcif']
        email = request.POST['txtemail']
        telefono = request.POST['txttel']
        web = request.POST['txtweb']
        cl = Cliente(nombre_empresa=nom, cif=cif,
                     email=email, telefono=telefono, web=web)
        try:
            cl.save()
        except IntegrityError:
            datos = {
                'r2': 'ERROR: El CIF ya está registrado'}
            return render(request, 'clientes/form_registrar_cl.html', datos)
        cl.save()
        datos = {
            'r': '¡Datos insertados correctamente del cliente: '+str(nom)+'!'}
        return render(request, 'clientes/form_registrar_cl.html', datos)

    else:
        # r2 variable que indica error
        datos = {'r2': "ERROR: No se puede insertar cliente"}
        return render(request, 'clientes/form_registrar_cl.html', datos)


def mostrarFormActualizarCl(request, id):
    try:
        cl = Cliente.objects.get(id=id)
        datos = {'cl': cl}
        return render(request, 'clientes/form_actualizar_cl.html', datos)

    except ObjectDoesNotExist:
        cl = Cliente.objects.all().values()
        datos = {'cl': cl,
                 'r2': 'El cliente con ID ('+str(id)+') no existe.'
                 }
        return render(request, 'clientes/listado_cl.html', datos)


def actualizarCl(request, id):
    try:
        cl = Cliente.objects.get(id=id)
    except ObjectDoesNotExist:
        datos = {'r2': '¡No se puede encontrar el cliente!'}
        return render(request, 'clientes/listado_cl.html', datos)

    if request.method == 'POST':
        nom = request.POST['txtnom']
        cif = request.POST['txtcif']
        email = request.POST['txtemail']
        telefono = request.POST['txttel']
        web = request.POST['txtweb']
        cl = Cliente.objects.get(id=id)

        # Comprueba que no haya otro cliente con el mismo CIF
        try:
            cliente_existente = Cliente.objects.exclude(id=id).get(cif=cif)
        except ObjectDoesNotExist:
            cliente_existente = None

        if cliente_existente:
            datos = {'r2': '¡Ya existe un cliente con ese CIF!'}
            return render(request, 'clientes/listado_cl.html', datos)

        cl.nombre_empresa = nom
        cl.cif = cif
        cl.email = email
        cl.telefono = telefono
        cl.web = web
        cl.save()
        cl = Cliente.objects.all().values()
        datos = {
            'cl': cl,
            'r': '¡Datos modificados correctamente del cliente: '+str(nom)+'!'
        }
        return render(request, 'clientes/listado_cl.html', datos)
    else:
        datos = {'r2': '¡No Se Puede Procesar Solicitud!'}
        return render(request, 'clientes/listado_cl.html', datos)


def eliminarCl(request, id):
    try:
        cl = Cliente.objects.get(id=id)
    except ObjectDoesNotExist:
        datos = {'r2': '¡No se puede encontrar el cliente!'}
        return render(request, 'clientes/listado_cl.html', datos)

    if request.method == 'POST':
        nom = cl.nombre_empresa
        cl.delete()
        messages.success(
            request, '¡El cliente {} ha sido eliminado correctamente!'.format(nom))
        return redirect('mostrarListadoCl')
        # datos = {'r': '¡El cliente ' +
        #          str(nom)+' ha sido eliminado correctamente!'}
        # return render(request, 'clientes/listado_cl.html', datos)

    datos = {'cl': cl}
    return render(request, 'clientes/form_eliminar_cl.html', datos)


# ---------------------------------------------------------------------------------------
# PRODUCTOS Y COMPRAS

def visualizarProd(request, id):
    prod = Producto.objects.get(id=id)
    datos = {'prod': prod}

    return render(request, 'productos/visualizar_prod.html', datos)


def mostrarListadoComp(request):
    order_by = request.GET.get('order_by')
    queryset = request.GET.get("buscar")

    comp = Compra.objects.all()

    if order_by == 'id_asc':
        comp = comp.order_by('id')
    elif order_by == 'id_desc':
        comp = comp.order_by('-id')
    elif order_by == 'cantidad_asc':
        comp = comp.order_by('cantidad')
    elif order_by == 'cantidad_desc':
        comp = comp.order_by('-cantidad')
    elif order_by == 'precio_asc':
        comp = comp.order_by('precio')
    elif order_by == 'precio_desc':
        comp = comp.order_by('-precio')
    elif order_by == 'fecha_asc':
        comp = comp.order_by('fecha')
    elif order_by == 'fecha_desc':
        comp = comp.order_by('-fecha')

    if queryset:
        comp = comp.filter(
            Q(id_producto__nombre__icontains=queryset) |
            Q(id_producto__referencia__icontains=queryset) |
            Q(id_usuario__username__icontains=queryset)
        ).distinct()

    for compra in comp:
        compra.precio_total = compra.cantidad * compra.precio

    # Paginación
    paginator = Paginator(comp, 15)
    current_page = request.GET.get('page', 1)
    comp_page = paginator.get_page(current_page)

    datos = {'comp': comp_page}
    return render(request, 'compras/listado_comp.html', datos)


def mostrarFormRegistrarCompNuevo(request):
    proveedores = Proveedor.objects.all()
    plano = Plano.objects.first()

    # Crear listas para pasillos, secciones y alturas
    pasillos_list = list(range(1, plano.pasillos + 1))
    secciones_list = list(range(1, plano.secciones + 1))
    alturas_list = list(range(1, plano.alturas + 1))

    datos = {'proveedores': proveedores,
             'plano': plano,
             'pasillos_list': pasillos_list,
             'secciones_list': secciones_list,
             'alturas_list': alturas_list
             }

    return render(request, 'compras/form_registrar_comp_nuevo.html', datos)


def insertarCompNuevo(request):
    if request.method == 'POST':
        ref = request.POST.get('txtref')
        proveedor_id = request.POST.get('proveedor')
        pasillo = request.POST.get('pasillo')
        seccion = request.POST.get('seccion')
        altura = request.POST.get('altura')

        proveedor = Proveedor.objects.get(id=proveedor_id)
        proveedores = Proveedor.objects.all()

        ubicacion = None
        if pasillo and seccion and altura and pasillo != '' and seccion != '' and altura != '':
            ubicacion, _ = Almacen.objects.get_or_create(
                pasillo=pasillo,
                seccion=seccion,
                altura=altura
            )

        try:
            Producto.objects.get(referencia=ref)
            datos = {
                'r2': 'ERROR: La referencia ya está registrada'
            }
            return render(request, 'compras/form_registrar_comp_nuevo.html', datos)
        except ObjectDoesNotExist:
            producto = Producto(
                referencia=ref,
                nombre=request.POST.get('txtnom'),
                tipo=request.POST.get('tipo'),
                precio_mayorista=request.POST.get('precio_may'),
                precio_minorista=request.POST.get('precio_min'),
                cantidad=request.POST.get('txtcant'),
                descripcion=request.POST.get('descripcion'),
                fotografia=request.FILES.get('fotografia'),
                id_proveedor=proveedor,
                id_ubicacion=ubicacion
            )

            producto.save()
            compra = Compra(
                id_producto=producto,
                cantidad=request.POST.get('txtcant'),
                precio=request.POST.get('precio_comp'),
                fecha=timezone.now(),
                id_usuario=request.user
            )
            compra.save()

        datos = {
            'r': '¡Datos insertados correctamente del producto: ' + str(producto.nombre) + '!',
            'proveedores': proveedores
        }
        return render(request, 'compras/form_registrar_comp_nuevo.html', datos)


def mostrarFormRegistrarCompExist(request):
    if 'comprobado' not in request.session:
        request.session['comprobado'] = False
    return render(request, 'compras/form_registrar_comp_exist.html')


def comprobarReferencia(request):
    referencia = request.GET.get('referencia', '')

    try:
        producto = Producto.objects.get(referencia=referencia)
    except Producto.DoesNotExist:
        datos = {
            'r2': 'La referencia no está registrada. Se trata de un producto nuevo.'
        }
        return render(request, 'compras/form_registrar_comp_exist.html', datos)

    request.session['comprobado'] = True
    datos = {
        'referencia': referencia,
        'producto': producto
    }
    return render(request, 'compras/form_registrar_comp_exist.html', datos)


def insertarCompExist(request):
    if request.method == 'POST':
        referencia = request.POST.get('referencia')
        cant = request.POST.get('cantidad')
        precio_comp = request.POST.get('precio_comp')

        try:
            comprobado = request.session['comprobado']
            del request.session['comprobado']
        except KeyError:
            comprobado = False

        if comprobado:
            try:
                producto = Producto.objects.get(referencia=referencia)
            except Producto.DoesNotExist:
                datos = {
                    'r2': 'La referencia no está registrada. Se trata de un producto nuevo.'
                }
                return render(request, 'compras/form_registrar_comp_exist.html', datos)

            producto = get_object_or_404(Producto, referencia=referencia)
            # Verificar que cantidad tenga un valor válido
            if cant is None:
                cant = 0
            else:
                cant = int(cant)

            if producto.cantidad is None:
                producto.cantidad = 0

            producto.cantidad += cant
            producto.save()

            compra = Compra(id_producto=producto, cantidad=cant,
                            precio=precio_comp, fecha=timezone.now(), id_usuario=request.user)
            compra.save()

            datos = {
                'r': '¡Datos insertados correctamente del producto: ' + str(producto.nombre) + '!'
            }
            return render(request, 'compras/form_registrar_comp_exist.html', datos)
        else:
            datos = {
                'r': 'Por favor, primero comprueba la referencia.'
            }
            return render(request, 'compras/form_registrar_comp_exist.html', datos)


def mostrarFormActualizarProd(request, id):
    try:
        prod = Producto.objects.get(id=id)
        proveedores = Proveedor.objects.all()
        plano = Plano.objects.first()

        # Crear listas para pasillos, secciones y alturas
        pasillos_list = list(range(1, plano.pasillos + 1))
        secciones_list = list(range(1, plano.secciones + 1))
        alturas_list = list(range(1, plano.alturas + 1))

        datos = {'prod': prod,
                'proveedores': proveedores,
                'pasillos_list': pasillos_list,
                'secciones_list': secciones_list,
                'alturas_list': alturas_list}

        return render(request, 'productos/form_actualizar_prod.html', datos)

    except ObjectDoesNotExist:
        datos = {'r2': 'El producto con ID (' + str(id) + ') no existe.'}
        return render(request, 'index.html', datos)


def actualizarProd(request, id):
    try:
        prod = Producto.objects.get(id=id)
    except ObjectDoesNotExist:
        datos = {'r2': '¡No se puede encontrar el producto!'}
        return render(request, 'index.html', datos)

    if request.method == 'POST':
        nom = request.POST.get('txtnom')
        ref = request.POST.get('txtref')
        cant = request.POST.get('txtcant')
        tipo = request.POST.get('tipo')
        precio_may = request.POST.get('precio_may')
        precio_min = request.POST.get('precio_min')
        descripcion = request.POST.get('descripcion')
        fotografia = request.FILES.get('fotografia')
        proveedor = request.POST.get('proveedor')
        pasillo = request.POST.get('pasillo')
        seccion = request.POST.get('seccion')
        altura = request.POST.get('altura')

        proveedor_obj = get_object_or_404(Proveedor, id=proveedor)

        if ref != prod.referencia:
            # Comprueba que no haya otro producto con la misma referencia
            try:
                producto_existente = Producto.objects.exclude(
                    id=id).get(referencia=ref)
            except ObjectDoesNotExist:
                producto_existente = None

            if producto_existente:
                datos = {'r2': '¡Ya existe un producto con esa referencia!'}
                return render(request, 'index.html', datos)
        else:
            prod.nombre = nom
            prod.referencia = ref
            prod.cantidad = cant
            prod.tipo = tipo
            prod.precio_mayorista = precio_may
            prod.precio_minorista = precio_min
            prod.descripcion = descripcion

            if fotografia:
                prod.fotografia = fotografia
            else:
                imagen_actual = request.POST.get('imagen_actual')
                prod.fotografia = imagen_actual

            prod.id_proveedor = proveedor_obj

            ubicacion = prod.id_ubicacion
            if ubicacion is not None:
                ubicacion.pasillo = pasillo
                ubicacion.seccion = seccion
                ubicacion.altura = altura
                ubicacion.save()
            else:
                ubicacion = None
                if pasillo and seccion and altura and pasillo != '' and seccion != '' and altura != '':
                    ubicacion = Almacen.objects.create(
                        # id=f'{pasillo}-{seccion}-{altura}',
                        pasillo=pasillo,
                        seccion=seccion,
                        altura=altura
                    )
            prod.id_ubicacion = ubicacion

            prod.save()

            messages.success(
                request, f'¡El producto {nom} ha sido modificado correctamente!')
            return redirect('/')

        datos = {'prod': prod}
        return render(request, 'productos/form_actualizar_prod.html', datos)


def eliminarProd(request, id):
    try:
        prod = Producto.objects.get(id=id)
    except ObjectDoesNotExist:
        datos = {'r2': '¡No se puede encontrar el producto!'}
        return render(request, 'index.html', datos)

    if request.method == 'POST':
        nom = prod.nombre
        prod.delete()
        # datos = {'r': '¡El producto ' + str(nom) + ' ha sido eliminado correctamente!'}
        messages.success(
            request, f'El producto {nom} ha sido eliminado correctamente!')

        return redirect('/')

    datos = {'prod': prod}
    return render(request, 'productos/form_eliminar_prod.html', datos)

# ---------------------------------------------------------------------------------------
# ALMACEN


def mostrarAlmacen(request):
    pasillo = request.GET.get('pasillo', '')
    seccion = request.GET.get('seccion', '')
    altura = request.GET.get('altura', '')

    plano = Plano.objects.first()
    productos = None

    if pasillo and seccion and altura:
        productos = Producto.objects.filter(
            id_ubicacion__pasillo=pasillo, id_ubicacion__seccion=seccion, id_ubicacion__altura=altura)
    elif pasillo and seccion:
        productos = Producto.objects.filter(
            id_ubicacion__pasillo=pasillo, id_ubicacion__seccion=seccion)
    elif pasillo:
        productos = Producto.objects.filter(id_ubicacion__pasillo=pasillo)
    else:
        productos = []

    # Paginación
    paginator = Paginator(productos, 4)
    current_page = request.GET.get('page', 1)
    prod_page = paginator.get_page(current_page)

    # Crear listas para pasillos, secciones y alturas
    pasillos_list = list(range(1, plano.pasillos + 1))
    secciones_list = list(range(1, plano.secciones + 1))
    alturas_list = list(range(1, plano.alturas + 1))

    datos = {
        'productos': prod_page,
        'plano': plano,
        'pasillos_list': pasillos_list,
        'secciones_list': secciones_list,
        'alturas_list': alturas_list
    }

    return render(request, 'almacen/almacen.html', datos)


def modificarAlmacen(request):
    if request.method == 'POST':
        
        imagen = request.FILES.get('plano')
        pasillos = int(request.POST.get('pasillos', 0))
        secciones = int(request.POST.get('secciones', 0))
        alturas = int(request.POST.get('alturas', 0))

        # Modifica el almacen actual
        plano = Plano.objects.get(pk=1)  # Obtener el objeto Plano existente
        plano.imagen = imagen
        plano.pasillos = pasillos
        plano.secciones = secciones
        plano.alturas = alturas
        plano.save()

        return redirect('mostrarAlmacen')

    return render(request, 'almacen/modificar_almacen.html')


# ---------------------------------------------------------------------------------------
# VENTAS


def mostrarFormRegistrarVenta(request, cliente=None):
    queryset = request.GET.get("buscar")

    if queryset:
        productos = Producto.objects.filter(
            Q(nombre__icontains=queryset) |
            Q(referencia__icontains=queryset) |
            Q(descripcion__icontains=queryset) |
            Q(id_proveedor__nombre_empresa__icontains=queryset)
        ).distinct()
    else:
        productos = Producto.objects.all()

    clientes = Cliente.objects.all()
    cliente_id = request.session.get('cliente_id')
    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
    else:
        cliente = None

    productos_seleccionados = request.session.get(
        'productos_seleccionados', [])

    # Calcular la suma de los precios totales
    total_sum = 0
    for producto in productos_seleccionados:
        total_sum += producto['precio_total']
    total_sum = round(total_sum, 2)

    datos = {
        'clientes': clientes,
        'cliente': cliente,
        'productos': productos,
        'productos_seleccionados': productos_seleccionados,
        'total_sum': total_sum,
    }
    return render(request, 'ventas/form_registrar_venta.html', datos)


def seleccionar_cliente(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')

        request.session['cliente_id'] = cliente_id

    return redirect('mostrarFormRegistrarVenta')


def seleccionar_producto(request, id):
    if request.method == 'POST':
        producto = Producto.objects.get(id=id)

        cantidad = int(request.POST['cantidad'])
        precio = request.POST.get('precio')
        fotografia = request.POST['fotografia']

        if cantidad > 0:
            cantidad = int(cantidad)
            precio = float(precio)
            precio_total = cantidad * precio
            precio_total = round(precio_total, 2)

        producto_seleccionado = {
            'id': producto.id,
            'referencia': producto.referencia,
            'nombre': producto.nombre,
            'cantidad': cantidad,
            'precio': precio,
            'precio_total': precio_total,
            'fotografia': fotografia,
        }

        productos_seleccionados = request.session.get(
            'productos_seleccionados', [])

        # Verificar si el producto ya está en la lista
        producto_existente = next(
            (p for p in productos_seleccionados if p['referencia'] == producto_seleccionado['referencia']), None)

        if producto_existente:
            messages.warning(request, 'El producto {} ya ha sido seleccionado'.format(
                producto_seleccionado['nombre']))
        else:
            productos_seleccionados.append(producto_seleccionado)
            request.session['productos_seleccionados'] = productos_seleccionados

    return redirect('mostrarFormRegistrarVenta')


def eliminar_seleccionado(request, id):
    productos_seleccionados = request.session.get(
        'productos_seleccionados', [])

    # Buscar el producto en la lista
    producto_existente = next(
        (p for p in productos_seleccionados if p['id'] == id), None)

    if producto_existente:
        productos_seleccionados.remove(producto_existente)
        request.session['productos_seleccionados'] = productos_seleccionados

    return redirect('mostrarFormRegistrarVenta')


def notificarCancelarVenta(request):
    if request.method == 'POST':
        return render(request, 'ventas/cancelar_venta.html')


def cancelarVenta(request):
    if request.method == 'POST':
        # Borrar las sesiones
        request.session.pop('cliente_id', None)
        request.session.pop('productos_seleccionados', None)

        return redirect('mostrarFormRegistrarVenta')

    return redirect('notificarCancelarVenta')


def realizarVenta(request):
    cliente_id = request.session.get('cliente_id')
    productos_seleccionados = request.session.get(
        'productos_seleccionados', [])
    productos_sin_stock = []

    for producto_seleccionado in productos_seleccionados:
        producto = Producto.objects.get(id=producto_seleccionado['id'])
        cantidad = producto_seleccionado['cantidad']
        precio = producto_seleccionado['precio']

        if cantidad > producto.cantidad:
            productos_sin_stock.append((producto.nombre, producto.cantidad))

    if productos_sin_stock:
        mensajes = []
        for producto in productos_sin_stock:
            mensaje = 'No hay suficiente stock disponible para el producto {}: Solo quedan {} unidades.'.format(
                producto[0], producto[1])
            mensajes.append(mensaje)

        mensajes_completos = '\n'.join(mensajes)
        lista_mensajes = linebreaksbr(mensajes_completos)
        messages.warning(request, lista_mensajes)
        return redirect('mostrarFormRegistrarVenta')

    venta = Venta.objects.create(
        id_cliente_id=cliente_id, id_usuario=request.user, fecha=timezone.now())

    for producto_seleccionado in productos_seleccionados:
        producto = Producto.objects.get(id=producto_seleccionado['id'])
        cantidad = producto_seleccionado['cantidad']
        precio = producto_seleccionado['precio']

        FilaVenta.objects.create(
            venta=venta, producto=producto, cantidad_venta=cantidad, precio_venta=precio)

        # Disminuir la cantidad del producto
        producto = Producto.objects.get(id=producto.id)
        producto.cantidad = producto.cantidad - cantidad
        producto.save()

    # Limpia las sesiones después de realizar la venta
    request.session['productos_seleccionados'] = []
    request.session['cliente_id'] = None

    return redirect('mostrarFactura', id=venta.id)


def mostrarListadoVenta(request):
    order_by = request.GET.get('order_by')
    queryset = request.GET.get("buscar")

    ventas = Venta.objects.all()

    if order_by == 'id_asc':
        ventas = ventas.order_by('id')
    elif order_by == 'id_desc':
        ventas = ventas.order_by('-id')
    elif order_by == 'fecha_asc':
        ventas = ventas.order_by('fecha')
    elif order_by == 'fecha_desc':
        ventas = ventas.order_by('-fecha')

    if queryset:
        ventas = ventas.filter(
            Q(id_cliente__nombre_empresa__icontains=queryset) |
            Q(id_producto__nombre__icontains=queryset) |
            Q(id_producto__referencia__icontains=queryset) |
            Q(id_usuario__username__icontains=queryset)
        ).distinct()

    paginator = Paginator(ventas, 15)
    current_page = request.GET.get('page', 1)
    venta_page = paginator.get_page(current_page)

    datos = {
        'ventas': venta_page,
        'filas_venta': [],
    }

    for venta in venta_page:
        total_sum = 0
        filas_venta = []
        for fila_venta in venta.filaventa_set.all():
            precio_total = fila_venta.cantidad_venta * fila_venta.precio_venta
            total_sum += precio_total
            filas_venta.append({
                'producto': fila_venta.producto,
                'cantidad_venta': fila_venta.cantidad_venta,
                'precio_venta': fila_venta.precio_venta,
                'precio_total': precio_total,
            })

        total_sum = round(total_sum, 2)
        venta.total_sum = total_sum
        datos['filas_venta'].extend(filas_venta)

    return render(request, 'ventas/listado_venta.html', datos)


def mostrarFactura(request, id):
    venta = Venta.objects.get(id=id)

    filas_venta = []
    total_venta = 0
    total_dev = 0

    for fila_venta in venta.filaventa_set.all():
        precio_total = fila_venta.cantidad_venta * fila_venta.precio_venta
        total_venta += precio_total
        filas_venta.append({
            'producto': fila_venta.producto,
            'cantidad_venta': fila_venta.cantidad_venta,
            'precio_venta': fila_venta.precio_venta,
            'precio_total': precio_total,
            'devolucion': False,
        })

    devoluciones = Devolucion.objects.filter(id_venta=venta)

    for devolucion in devoluciones:
        filas_devolucion = FilaDevolucion.objects.filter(devolucion=devolucion)

        for fila_devolucion in filas_devolucion:
            fila_venta = FilaVenta.objects.get(
                venta=venta, producto=fila_devolucion.producto)

            precio_total_devolucion = fila_devolucion.cantidad_devuelta * fila_venta.precio_venta
            total_dev += precio_total_devolucion
            filas_venta.append({
                'producto': fila_devolucion.producto,
                'cantidad_venta': fila_devolucion.cantidad_devuelta,
                'precio_venta': fila_venta.precio_venta,
                'precio_total': -precio_total_devolucion,
                'devolucion': True,
                'fecha_devolucion': devolucion.fecha,
                'razon_devolucion': devolucion.razon,
            })

    total_venta = round(total_venta, 2)
    iva = total_venta * Decimal('0.21')
    iva = round(iva, 2)
    subtotal = total_venta - iva
    subtotal = round(subtotal, 2)
    total = total_venta - total_dev
    total = round(total, 2)

    datos = {
        'venta': venta,
        'iva': iva,
        'subtotal': subtotal,
        'total': total,
        'total_dev': total_dev,
        'total_venta': total_venta,
        'filas_venta': filas_venta,
    }

    return render(request, 'ventas/factura.html', datos)


# ---------------------------------------------------------------------------------------
# REPOSICION

def mostrarListadoReposicion(request):
    queryset = request.GET.get("buscar")
    cantidad_reposicion = int(request.GET.get('cantidad_reposicion', 20))
    productos = Producto.objects.filter(cantidad__lt=cantidad_reposicion)

    if queryset:
        productos = productos.filter(
            Q(nombre__icontains=queryset) |
            Q(referencia__icontains=queryset) |
            Q(descripcion__icontains=queryset) |
            Q(id_proveedor__nombre_empresa__icontains=queryset)
        ).distinct()

    # Paginación
    paginator = Paginator(productos, 4)
    current_page = request.GET.get('page', 1)
    reposicion_page = paginator.get_page(current_page)

    datos = {
        'productos': reposicion_page,
        'cantidad_reposicion': cantidad_reposicion}
    return render(request, 'listado_reposicion.html', datos)


# ---------------------------------------------------------------------------------------
# DEVOLUCION


def realizarDevolucion(request, id):
    venta = Venta.objects.get(id=id)

    filas_venta = []
    total_sum = 0

    for fila_venta in venta.filaventa_set.all():
        precio_total = fila_venta.cantidad_venta * fila_venta.precio_venta
        total_sum += precio_total
        filas_venta.append({
            'producto': fila_venta.producto,
            'cantidad_venta': fila_venta.cantidad_venta,
            'precio_venta': fila_venta.precio_venta,
            'precio_total': precio_total,
        })

    total_sum = round(total_sum, 2)
    iva = total_sum * Decimal('0.21')
    iva = round(iva, 2)
    subtotal = total_sum - iva
    subtotal = round(subtotal, 2)

    productos_devueltos = request.session.get('productos_devueltos', [])

    datos = {
        'venta': venta,
        'iva': iva,
        'subtotal': subtotal,
        'total_sum': total_sum,
        'filas_venta': filas_venta,
        'productos_devueltos': productos_devueltos,
    }

    return render(request, 'devoluciones/devolucion.html', datos)


def devolver_producto(request, venta_id, producto_id):
    productos_devueltos = request.session.get('productos_devueltos', [])

    if request.method == 'POST':
        producto = Producto.objects.get(id=producto_id)

        cantidad = int(request.POST['cant_devolver'])
        precio = request.POST.get('producto_precio')

        if cantidad > 0 and cantidad < producto.cantidad:
            cantidad = int(cantidad)
            precio = float(precio)
            precio_total = cantidad * precio
            precio_total = round(precio_total, 2)

            producto_devuelto = {
                'id': producto.id,
                'referencia': producto.referencia,
                'nombre': producto.nombre,
                'cantidad': cantidad,
                'precio': precio,
                'precio_total': precio_total,
            }

            producto_existente = next(
                (p for p in productos_devueltos if p['referencia'] == producto_devuelto['referencia']), None)

            if producto_existente:
                messages.warning(request, 'El producto {} ya ha sido devuelto'.format(
                    producto_devuelto['nombre']))
            else:
                productos_devueltos.append(producto_devuelto)
                request.session['productos_devueltos'] = productos_devueltos

    redirect_url = reverse('realizarDevolucion', args=[venta_id])
    return redirect(redirect_url)


def eliminar_devuelto(request, id, venta_id):
    productos_devueltos = request.session.get(
        'productos_devueltos', [])

    # Buscar el producto en la lista
    producto_existente = next(
        (p for p in productos_devueltos if p['id'] == id), None)

    if producto_existente:
        productos_devueltos.remove(producto_existente)
        request.session['productos_devueltos'] = productos_devueltos

    redirect_url = reverse('realizarDevolucion', args=[venta_id])
    return redirect(redirect_url)


def cancelarDevolucion(request, id):
    if request.method == 'POST':
        # Borrar las sesiones
        request.session.pop('productos_devueltos', None)

        return redirect('mostrarFactura', id=id)


def confirmarDevolucion(request, id):
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        motivo_otro = request.POST.get('motivoOtro', '')
        motivo = motivo_otro if motivo == 'otro' else motivo

        if motivo == 'otro' and not motivo_otro:
            messages.warning(
                request, 'Debe especificar el motivo de devolución')
            return redirect('realizarDevolucion', id=id)

        venta = Venta.objects.get(id=id)

        devolucion = Devolucion.objects.create(
            id_venta=venta, razon=motivo, fecha=timezone.now(), id_usuario=request.user)

        # Obtener los productos devueltos de la sesión
        productos_devueltos = request.session.get('productos_devueltos', [])

        # Guardar los productos devueltos en la tabla FilaDevolucion
        for producto_devuelto in productos_devueltos:
            producto = Producto.objects.get(id=producto_devuelto['id'])
            cantidad_devuelta = producto_devuelto['cantidad']
            FilaDevolucion.objects.create(
                devolucion=devolucion, producto=producto, cantidad_devuelta=cantidad_devuelta)

            producto.cantidad += cantidad_devuelta
            producto.save()

        # Borrar las sesiones
        request.session.pop('productos_devueltos', None)

        return redirect('mostrarFactura', id=id)

    return redirect('realizarDevolucion', id=id)


def mostrarListadoDevoluciones(request):
    order_by = request.GET.get('order_by')
    queryset = request.GET.get("buscar")

    devoluciones_all = Devolucion.objects.all()

    if order_by == 'id_asc':
        devoluciones_all = devoluciones_all.order_by('id')
    elif order_by == 'id_desc':
        devoluciones_all = devoluciones_all.order_by('-id')
    elif order_by == 'fecha_asc':
        devoluciones_all = devoluciones_all.order_by('fecha')
    elif order_by == 'fecha_desc':
        devoluciones_all = devoluciones_all.order_by('-fecha')

    if queryset:
        devoluciones_all = devoluciones_all.filter(
            Q(id_venta__id_cliente__nombre_empresa__icontains=queryset) |
            Q(id_venta__id_producto__nombre__icontains=queryset) |
            Q(id_venta__id_producto__referencia__icontains=queryset) |
            Q(id_usuario__username__icontains=queryset)
        ).distinct()

    paginator = Paginator(devoluciones_all, 15)
    current_page = request.GET.get('page', 1)
    devoluciones = paginator.get_page(current_page)

    datos = {
        'devoluciones': devoluciones,
        'filas_devolucion': [],
        'ventas_ids': [],
    }

    for devolucion in devoluciones:
        total_sum = 0
        filas_devolucion = []
        for fila_devolucion in devolucion.filadevolucion_set.all():
            fila_venta = FilaVenta.objects.get(
                venta=devolucion.id_venta, producto=fila_devolucion.producto)
            precio_total = fila_devolucion.cantidad_devuelta * \
                fila_venta.precio_venta
            total_sum += precio_total
            filas_devolucion.append({
                'producto': fila_devolucion.producto,
                'cantidad_devolucion': fila_devolucion.cantidad_devuelta,
                'precio_devolucion': fila_venta.precio_venta,
                'precio_total': precio_total,
            })

        total_sum = round(total_sum, 2)
        devolucion.total_sum = total_sum

        # cliente = None
        # if devolucion.id_venta.id_cliente:
        #     cliente = devolucion.id_venta.id_cliente.nombre_empresa

        datos['filas_devolucion'].extend(filas_devolucion)
        datos['ventas_ids'].append(devolucion.id_venta.id)

    return render(request, 'devoluciones/listado_dev.html', datos)

# ---------------------------------------------------------------------------------------
# CUENTA DE RESULTADOS


def cuentaResultados(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')

        try:
            if isinstance(fecha, str):
                fecha = datetime.strptime(fecha, '%Y-%m-%d')

            if 'dia_anterior' in request.POST:
                fecha -= timedelta(days=1)
            elif 'dia_siguiente' in request.POST:
                fecha += timedelta(days=1)

            ventas = Venta.objects.filter(fecha__date=fecha).aggregate(
                total_ventas=Sum(F('filaventa__precio_venta') * F('filaventa__cantidad_venta')))
            devoluciones = Devolucion.objects.filter(fecha__date=fecha).aggregate(
                total_devoluciones=Sum('id_venta__filaventa__precio_venta'))
            compras = Compra.objects.filter(fecha__date=fecha).aggregate(
                total_compras=Sum(F('cantidad') * F('precio')))

            total_ventas = ventas['total_ventas'] if ventas['total_ventas'] is not None else 0
            total_devoluciones = devoluciones['total_devoluciones'] if devoluciones['total_devoluciones'] is not None else 0
            total_compras = compras['total_compras'] if compras['total_compras'] is not None else 0

            resultado = total_ventas - total_devoluciones - total_compras

            datos = {
                'fecha': fecha,
                'ventas': total_ventas,
                'devoluciones': total_devoluciones,
                'compras': total_compras,
                'resultado': resultado,
                'resultados': True
            }

            return render(request, 'cuenta_resultados.html', datos)

        except ValueError:
            error = 'Fecha inválida. El formato debe ser DD-MM-AAAA.'
            messages.error(request, error)
            return render(request, 'cuenta_resultados.html')

    return render(request, 'cuenta_resultados.html')


def cuentaMensual(request):
    if request.method == 'POST':
        mes = int(request.POST.get('mes'))
        anio = int(request.POST.get('anio'))

        try:
            if 'mes_anterior' in request.POST:
                if mes == 1:
                    mes = 12
                else:
                    mes -= 1
            elif 'mes_siguiente' in request.POST:
                if mes == 12:
                    mes = 1
                else:
                    mes += 1

            _, last_day = monthrange(anio, mes)
            fecha_inicio = datetime(anio, mes, 1)
            fecha_fin = datetime(anio, mes, last_day)

            ventas = Venta.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(
                total_ventas=Sum(F('filaventa__precio_venta') * F('filaventa__cantidad_venta')))
            devoluciones = Devolucion.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(
                total_devoluciones=Sum('id_venta__filaventa__precio_venta'))
            compras = Compra.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(
                total_compras=Sum(F('cantidad') * F('precio')))

            total_ventas = ventas['total_ventas'] if ventas['total_ventas'] is not None else 0
            total_devoluciones = devoluciones['total_devoluciones'] if devoluciones['total_devoluciones'] is not None else 0
            total_compras = compras['total_compras'] if compras['total_compras'] is not None else 0

            resultado = total_ventas - total_devoluciones - total_compras

            datos = {
                'mes': mes,
                'anio': anio,
                'ventas': total_ventas,
                'devoluciones': total_devoluciones,
                'compras': total_compras,
                'resultado': resultado,
                'resultados': True
            }

            return render(request, 'cuenta_mensual.html', datos)

        except ValueError:
            error = 'Fecha inválida.'
            messages.error(request, error)
            return render(request, 'cuenta_mensual.html')

    return render(request, 'cuenta_mensual.html')

# ---------------------------------------------------------------------------------------
# LISTADO DE PRECIOS


def listadoPrecioMin(request):
    queryset = request.GET.get("buscar")
    order_by = request.GET.get('order_by')
    tipo_seleccionado = request.GET.get('tipo')

    prod = Producto.objects.all()

    if queryset:
        prod = prod.filter(
            Q(nombre__icontains=queryset) |
            Q(referencia__icontains=queryset) |
            Q(descripcion__icontains=queryset)
        ).distinct()

    if tipo_seleccionado:
        prod = prod.filter(tipo=tipo_seleccionado)

    if order_by == 'nombre_asc':
        prod = prod.order_by('nombre')
    elif order_by == 'nombre_desc':
        prod = prod.order_by('-nombre')
    elif order_by == 'precio_minorista_asc':
        prod = prod.order_by('precio_minorista')
    elif order_by == 'precio_minorista_desc':
        prod = prod.order_by('-precio_minorista')
    elif order_by == 'referencia_asc':
        prod = prod.order_by('referencia')
    elif order_by == 'referencia_desc':
        prod = prod.order_by('-referencia')

    tipos_producto = ["", "techo", "aplique", "plafon",
                      "flexos", "pie", "infantil", "exterior", "ventiladores"]

    datos = {
        'prod': prod,
        'tipos_producto': tipos_producto,
        'tipo_seleccionado': tipo_seleccionado,
    }

    return render(request, 'lista_precios/lista_precio_min.html', datos)


def listadoPrecioMay(request):
    queryset = request.GET.get("buscar")
    order_by = request.GET.get('order_by')
    tipo_seleccionado = request.GET.get('tipo')

    prod = Producto.objects.all()

    if queryset:
        prod = prod.filter(
            Q(nombre__icontains=queryset) |
            Q(referencia__icontains=queryset) |
            Q(descripcion__icontains=queryset)
        ).distinct()

    if tipo_seleccionado:
        prod = prod.filter(tipo=tipo_seleccionado)

    if order_by == 'nombre_asc':
        prod = prod.order_by('nombre')
    elif order_by == 'nombre_desc':
        prod = prod.order_by('-nombre')
    elif order_by == 'precio_mayorista_asc':
        prod = prod.order_by('precio_mayorista')
    elif order_by == 'precio_mayorista_desc':
        prod = prod.order_by('-precio_mayorista')
    elif order_by == 'referencia_asc':
        prod = prod.order_by('referencia')
    elif order_by == 'referencia_desc':
        prod = prod.order_by('-referencia')

    tipos_producto = ["", "techo", "aplique", "plafon",
                      "flexos", "pie", "infantil", "exterior", "ventiladores"]

    datos = {
        'prod': prod,
        'tipos_producto': tipos_producto,
        'tipo_seleccionado': tipo_seleccionado,
    }

    return render(request, 'lista_precios/lista_precio_may.html', datos)
