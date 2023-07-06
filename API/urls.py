from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required


from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.mostrarIndex),
   
    # Proveedores
    path('form_registrar_prov', staff_member_required(views.mostrarFormRegistrarProv)),
    path('listado_prov', staff_member_required(views.mostrarListadoProv), name='mostrarListadoProv'),
    path('insertar_prov', staff_member_required(views.insertarProv)),
    path('form_actualizar_prov/<int:id>', staff_member_required(views.mostrarFormActualizarProv)),
    path('actualizar_prov/<int:id>', staff_member_required(views.actualizarProv)),
    path('form_eliminar_prov/<int:id>', staff_member_required(views.eliminarProv)),


    # Clientes
    path('form_registrar_cl', views.mostrarFormRegistrarCl),
    path('listado_cl', views.mostrarListadoCl, name='mostrarListadoCl'),
    path('insertar_cl', views.insertarCl),
    path('form_actualizar_cl/<int:id>', views.mostrarFormActualizarCl),
    path('actualizar_cl/<int:id>', views.actualizarCl),
    path('eliminar_cl/<int:id>', views.eliminarCl),
    path('form_eliminar_cl/<int:id>', views.eliminarCl),

    # Productos
    path('form_actualizar_prod/<int:id>', views.mostrarFormActualizarProd),
    path('actualizar_prod/<int:id>', views.actualizarProd),
    path('form_eliminar_prod/<int:id>', views.eliminarProd),
    path('visualizar_prod/<int:id>', views.visualizarProd),

    #Almacen
    path('almacen', views.mostrarAlmacen, name='mostrarAlmacen'),
    path('modificar_almacen', staff_member_required(views.modificarAlmacen)),

    # Compras
    path('form_registrar_comp_nuevo', staff_member_required(views.mostrarFormRegistrarCompNuevo)),
    path('form_registrar_comp_exist', staff_member_required(views.mostrarFormRegistrarCompExist)),
    path('comprobarReferencia/', staff_member_required(views.comprobarReferencia)),
    path('insertar_comp_nuevo', staff_member_required(views.insertarCompNuevo)),
    path('insertar_comp_exist', staff_member_required(views.insertarCompExist)),
    path('listado_comp', staff_member_required(views.mostrarListadoComp)),

    # Ventas
    path('form_registrar_venta', views.mostrarFormRegistrarVenta, name='mostrarFormRegistrarVenta'),
    path('form_registrar_venta/<int:cliente>/', views.mostrarFormRegistrarVenta, name='mostrarFormRegistrarVenta'),
    path('realizar_venta', views.realizarVenta, name="realizarVenta"),
    path('mostrar_factura/<int:id>', views.mostrarFactura, name="mostrarFactura"),
    path('seleccionar_cliente', views.seleccionar_cliente),
    path('seleccionar_producto/<int:id>', views.seleccionar_producto),
    path('eliminar_seleccionado/<int:id>', views.eliminar_seleccionado),
    path('cancelar_venta', views.cancelarVenta, name="cancelarVenta"),
    path('notificar_cancelar_venta', views.notificarCancelarVenta, name="notificarCancelarVenta"),
    path('listado_venta', views.mostrarListadoVenta, name="mostrarListadoVenta"),

    # Devolucion
    path('realizar_devolucion/<int:id>/', views.realizarDevolucion, name="realizarDevolucion"),
    path('devolver_producto/<int:venta_id>/<int:producto_id>', views.devolver_producto, name="devolverProducto"),
    path('eliminar_devuelto/<int:id>/<int:venta_id>', views.eliminar_devuelto),
    path('cancelar_devolucion/<int:id>', views.cancelarDevolucion, name="cancelarDevolucion"),
    path('confirmar_devolucion/<int:id>', views.confirmarDevolucion, name="confirmarDevolucion"),
    path('listado_dev', views.mostrarListadoDevoluciones),

    # Aviso reposición
    path('listado_reposicion', views.mostrarListadoReposicion, name="mostrarListadoReposicion"),
    
    # Cuenta de resultados
    path('cuenta_resultados', views.cuentaResultados, name="cuentaResultados"),
    path('cuenta_mensual', views.cuentaMensual, name="cuentaMensual"),


    #Listado precio
    path('lista_precio_min', views.listadoPrecioMin, name="listadoPrecioMin"),
    path('lista_precio_may', views.listadoPrecioMay, name="listadoPrecioMay"),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

