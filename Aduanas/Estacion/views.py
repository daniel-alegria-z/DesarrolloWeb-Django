from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.hashers import *
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .decorators import *

# Create your views here.
def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')

def registro_exitoso2(request):
    return render(request, 'registro_exitoso2.html')

def modificacion_exitosa(request):
    return render(request, 'modificacion_exitosa.html')

def inicio(request):
    return render(request, 'inicio.html')


def iniciar_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(correo=email)
            if usuario.contrasena == password:  # Verificación básica
                request.session['usuario_id'] = usuario.id
                request.session['usuario_rol'] = usuario.rol  # Guarda el rol en la sesión

                # Redirigir según el rol
                if usuario.rol == 'Administrador':
                    return redirect('servicios')  # Página para administrador
                elif usuario.rol == 'Supervisor':
                    return redirect('servicios_supervisor')  # Página para supervisor

            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "Correo no encontrado.")

    return render(request, 'iniciar_sesion.html')


def cerrar_sesion(request):
    request.session.flush()  # Elimina toda la información de la sesión
    messages.success(request, "Sesión cerrada con éxito.")
    return redirect('/Estacion/iniciar_sesion/')

# Vista protegida para administradores
@require_role('Administrador')
def servicios(request):
    return render(request, 'servicios.html')

# Vista protegida para supervisores
@require_role('Supervisor')
def servicios_supervisor(request):
    return render(request, 'servicios_supervisor.html')

# Vista genérica para acceso denegado
def desautorizado(request):
    return render(request, 'desautorizado.html')

@require_role('Administrador')
def registro_usuario(request):
    if request.method == 'POST':  
        Usuario.objects.create(
            nombreCompleto=request.POST.get('name'),
            telefono=request.POST.get('contact'),
            correo=request.POST.get('email'),
            contrasena=request.POST.get('password'),
            ano_nacimiento=request.POST.get('dob'),
            pais=request.POST.get('country'),
            rol=request.POST.get('role'),
            genero=request.POST.get('gender')
        )  
        return redirect('registro_exitoso2')
    return render(request, 'registro_usuario.html')

def registro_usuario_is(request):
    if request.method == 'POST':  
        Usuario.objects.create(
            nombreCompleto=request.POST.get('name'),
            telefono=request.POST.get('contact'),
            correo=request.POST.get('email'),
            contrasena=request.POST.get('password'),
            ano_nacimiento=request.POST.get('dob'),
            pais=request.POST.get('country'),
            rol=request.POST.get('role'),
            genero=request.POST.get('gender')
        )  
        return redirect('registro_exitoso')
    return render(request, 'registro_usuario_is.html')

@require_role('Administrador')
def modificar_usuario(request):
    usuarios = Usuario.objects.all()
    user_data = None 

    usuario_id = request.session.get('selected_usuario_id', None) or request.GET.get('usuario_id')

    if usuario_id:
        try:
            user_data = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            user_data = None
        finally:
            if 'selected_usuario_id' in request.session:
                del request.session['selected_usuario_id']
    
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id') 
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                usuario.nombreCompleto = request.POST.get('name')
                usuario.telefono = request.POST.get('contact')
                usuario.correo = request.POST.get('email')
                usuario.ano_nacimiento = request.POST.get('dob')
                usuario.pais = request.POST.get('country')
                usuario.rol = request.POST.get('role')
                usuario.genero = request.POST.get('gender')
                usuario.save() 
                return redirect('modificacion_exitosa') 
            except Usuario.DoesNotExist:
                return render(request, 'modificar_usu.html', {
                    'usuarios': usuarios,
                    'error': 'Usuario no encontrado.',
                    'user_data': user_data
                })

    elif request.method == 'GET':
        usuario_id = request.GET.get('usuario_id') 
        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)  
                return JsonResponse({
                    'name': usuario.nombreCompleto,
                    'contact': usuario.telefono,
                    'email': usuario.correo,
                    'dob': usuario.ano_nacimiento,
                    'country': usuario.pais,
                    'role': usuario.rol,
                    'gender': usuario.genero
                })
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'No se encontró el usuario.'}, status=404)


    return render(request, 'modificar_usu.html', {
        'usuarios': usuarios,
        'user_data': user_data  
    })

@require_role('Administrador')
def consultar_usuario(request):
    usuarios = Usuario.objects.all()
    user_data = None

    usuario_id = request.GET.get('usuario_id', None)
    if usuario_id:
        try:
            user_data = Usuario.objects.get(id=usuario_id)
            request.session['selected_usuario_id'] = usuario_id
        except Usuario.DoesNotExist:
            user_data = None
            if 'selected_usuario_id' in request.session:
                del request.session['selected_usuario_id']

    return render(request, 'consultar_usuario.html', {'usuarios': usuarios, 'user_data': user_data})

@require_role('Supervisor')
def consultar_usuarioS(request):
    usuarios = Usuario.objects.all()
    user_data = None

    usuario_id = request.GET.get('usuario_id', None)
    if usuario_id:
        try:
            user_data = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            user_data = None

    return render(request, 'consultar_usuarioS.html', {'usuarios': usuarios, 'user_data': user_data})


@require_role('Administrador')
def listar_usuarios(request):
    # Inicializa la consulta de todos los usuarios
    usuarios = Usuario.objects.all()

    rol_filtro = request.GET.get('rol', None)
    if rol_filtro:
        usuarios = usuarios.filter(rol__icontains=rol_filtro)

    # Si se pasa un usuario_id, obtener un solo usuario
    usuario_id = request.GET.get('usuario_id', None)
    user_data = None
    if usuario_id:
        try:
            user_data = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            user_data = None

    # Renderizar la vista con los resultados filtrados
    return render(request, 'listar_usuarios.html', {
        'usuarios': usuarios,
        'user_data': user_data,
        'rol_filtro': rol_filtro,
    })


@require_role('Supervisor')
def listar_usuariosS(request):
    # Inicializa la consulta de todos los usuarios
    usuarios = Usuario.objects.all()

    rol_filtro = request.GET.get('rol', None)
    if rol_filtro:
        usuarios = usuarios.filter(rol__icontains=rol_filtro)

    # Si se pasa un usuario_id, obtener un solo usuario
    usuario_id = request.GET.get('usuario_id', None)
    user_data = None
    if usuario_id:
        try:
            user_data = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            user_data = None

    # Renderizar la vista con los resultados filtrados
    return render(request, 'listar_usuariosS.html', {
        'usuarios': usuarios,
        'user_data': user_data,
        'rol_filtro': rol_filtro,
    })

@require_role('Administrador')
def eliminar_usuario(request):
    usuarios = Usuario.objects.all()  # Obtiene todos los usuarios
    eliminado = None  # Variable para verificar si se eliminó correctamente
    if request.method == "POST":
        usuario_id = request.POST.get('usuario_id') 
        try:
            usuario = Usuario.objects.get(id=usuario_id)

            UsuarioBorrado.objects.create(
                id = usuario_id,
                nombreCompleto=usuario.nombreCompleto, 
                rol=usuario.rol,
                contrasena=usuario.contrasena,
                ano_nacimiento=usuario.ano_nacimiento,
                pais=usuario.pais,
                telefono=usuario.telefono,
                correo=usuario.correo,
                genero=usuario.genero
            )

            usuario.delete()
            eliminado = True
        except Usuario.DoesNotExist:
            eliminado = False
            
    return render(request, 'eliminar_usuario.html', {'usuarios': usuarios, 'eliminado': eliminado})

@require_role('Administrador')
def registro_importacion(request):
    transportes = Transporte.objects.all() 
    responsables = Usuario.objects.all() 
    if request.method == 'POST':  
        transporte = get_object_or_404(Transporte, idTransporte=request.POST.get('transport_id'))
        responsable = get_object_or_404(Usuario, id=request.POST.get('responsible_id'))
        Importacion.objects.create(
            idImportacion=request.POST.get('import_id'),
            fechaDeclaracion=request.POST.get('declaration_date'),
            proveedor=request.POST.get('supplier'),
            descripcionMercancia=request.POST.get('description'),
            codigoArancelario=request.POST.get('tariff_code'),
            cantidad=request.POST.get('quantity'),
            unidadMedida=request.POST.get('unit'),
            valorCif=request.POST.get('cif_value'),
            impuestos=request.POST.get('taxes'),
            origenMercancia=request.POST.get('origin_country'),
            puertoEntrada=request.POST.get('entry_port'),
            transporteID=transporte,
            responsableID=responsable,
        )  
        return redirect('registro_exitoso2')
    return render(request, 'registro_importacion.html',{'transportes': transportes, 'responsables': responsables})

@require_role('Administrador')
def modificar_importacion(request):
    # Obtén todas las importaciones para mostrar en el campo de selección
    importaciones = Importacion.objects.all()
    transportes = Transporte.objects.all() 
    responsables = Usuario.objects.all() 
    importacion = None  # Inicializa como None
    
    import_data = None
    import_id = request.session.get('selected_import_id', None) or request.GET.get('import_id')
    
    if import_id:
        try:
            import_data = Importacion.objects.get(idImportacion = import_id)
        except Importacion.DoesNotExist:
            import_data = None
        finally:
            if 'selected_import_id' in request.session:
                del request.session['selected_import_id']
    
    if request.method == 'POST':
        import_id = request.POST.get('import_id')  # Obtiene el ID de importación del formulario
        if import_id:
            try:
                # Busca la importación por su ID
                importacion = Importacion.objects.get(idImportacion=import_id)
                
                # Actualiza los campos con los nuevos valores del formulario
                importacion.fechaDeclaracion = request.POST.get('declaration_date')
                importacion.proveedor = request.POST.get('supplier')
                importacion.descripcionMercancia = request.POST.get('description')
                importacion.codigoArancelario = request.POST.get('tariff_code')
                importacion.cantidad = request.POST.get('quantity')
                importacion.unidadMedida = request.POST.get('unit')
                importacion.valorCif = request.POST.get('cif_value')
                importacion.impuestos = request.POST.get('taxes')
                importacion.origenMercancia = request.POST.get('origin_country')
                importacion.puertoEntrada = request.POST.get('entry_port')
                
                # Actualiza los IDs de transporte y responsable
                transporte_id = request.POST.get('transport_id')
                responsable_id = request.POST.get('responsible_id')
                
                if transporte_id:
                    transporte = get_object_or_404(Transporte, idTransporte=transporte_id)
                    importacion.transporteID = transporte
                if responsable_id:
                    responsable = get_object_or_404(Usuario, id=responsable_id)
                    importacion.responsableID = responsable

                importacion.save()  # Guarda los cambios en la base de datos
                return redirect('modificacion_exitosa')
            except Importacion.DoesNotExist:
                return render(request, 'modificar_importacion.html', {
                    'importaciones': importaciones,
                    'transportes': transportes,
                    'responsables': responsables,
                    'error': 'Importación no encontrada.',
                    'import_data': import_data
                })

    # Manejo de la petición GET para cargar los datos de la importación seleccionada
    if request.method == 'GET':
        import_id = request.GET.get('import_id')  # Obtiene el ID del parámetro de consulta
        if import_id:
            try:
                # Busca la importación por su ID
                importacion = Importacion.objects.get(idImportacion=import_id)
                return JsonResponse({
                    'declaration_date': importacion.fechaDeclaracion,
                    'supplier': importacion.proveedor,
                    'description': importacion.descripcionMercancia,
                    'tariff_code': importacion.codigoArancelario,
                    'quantity': importacion.cantidad,
                    'unit': importacion.unidadMedida,
                    'cif_value': importacion.valorCif,
                    'taxes': importacion.impuestos,
                    'origin_country': importacion.origenMercancia,
                    'entry_port': importacion.puertoEntrada,
                    'transport_id': importacion.transporteID.idTransporte if importacion.transporteID else None,
                    'responsible_id': importacion.responsableID.id if importacion.responsableID else None
                })
            except Importacion.DoesNotExist:
                return JsonResponse({'error': 'No se encontró la importación.'}, status=404)

    return render(request, 'modificar_importacion.html', {
        'importaciones': importaciones,
        'importacion': importacion,
        'transportes': transportes,
        'responsables': responsables,
        'import_data': import_data
    })

@require_role('Administrador')
def consultar_importacion(request):
    importaciones = Importacion.objects.all()
    import_data = None

    import_id = request.GET.get('import_id', None)

    if import_id:
        try:
            import_data = Importacion.objects.get(idImportacion=import_id)
            request.session['selected_import_id'] = import_id
        except Importacion.DoesNotExist:
            import_data = None
            if 'selected_import_id' in request.session:
                del request.session['selected_import_id']

    return render(request, 'consultar_importacion.html', {'importaciones': importaciones, 'import_data': import_data})


@require_role('Supervisor')
def consultar_importacionS(request):
    importaciones = Importacion.objects.all()
    impo_data = None

    import_id = request.GET.get('import_id', '').strip()

    if import_id.isdigit():
        try:
            impo_data = Importacion.objects.get(idImportacion=import_id)
        except Importacion.DoesNotExist:
            impo_data = None
    else:
        impo_data = None

    return render(request, 'consultar_importacionS.html', {'importaciones': importaciones, 'impo_data': impo_data})


@require_role('Administrador')
def listar_importaciones(request):
    importaciones = Importacion.objects.all()  # Obtén todas las importaciones
    return render(request, 'listar_importaciones.html', {'importaciones': importaciones})

@require_role('Supervisor')
def listar_importacionS(request):
    importaciones = Importacion.objects.all()  # Obtén todas las importaciones
    return render(request, 'listar_importacionS.html', {'importaciones': importaciones})


@require_role('Administrador')
def eliminar_importacion(request):
    importaciones = Importacion.objects.all()  # Obtén todas las importaciones
    eliminado = None

    if 'import_id' in request.POST:
        import_id = request.POST['import_id']
        try:
            importacion_a_eliminar = Importacion.objects.get(idImportacion=import_id)
            
            # Crear un registro en Importacion_borrada
            ImportacionBorrada.objects.create(
                idImportacion=importacion_a_eliminar.idImportacion,
                fechaDeclaracion=importacion_a_eliminar.fechaDeclaracion,
                proveedor=importacion_a_eliminar.proveedor,
                descripcionMercancia=importacion_a_eliminar.descripcionMercancia,
                codigoArancelario=importacion_a_eliminar.codigoArancelario,
                cantidad=importacion_a_eliminar.cantidad,
                unidadMedida=importacion_a_eliminar.unidadMedida,
                valorCif=importacion_a_eliminar.valorCif,
                impuestos=importacion_a_eliminar.impuestos,
                origenMercancia=importacion_a_eliminar.origenMercancia,
                puertoEntrada=importacion_a_eliminar.puertoEntrada,
                transporteID=importacion_a_eliminar.transporteID,
                responsableID=importacion_a_eliminar.responsableID
            )

            # Eliminar la importación
            importacion_a_eliminar.delete()
            eliminado = True
        except Importacion.DoesNotExist:
            eliminado = False

    return render(request, 'eliminar_importacion.html', {'importaciones': importaciones, 'eliminado': eliminado})



@require_role('Administrador')
def registro_exportacion(request):
    transportes = Transporte.objects.all() 
    responsables = Usuario.objects.all() 
    if request.method == 'POST':  
        transporte = get_object_or_404(Transporte, idTransporte=request.POST.get('transport_id'))
        responsable = get_object_or_404(Usuario, id=request.POST.get('responsible_id'))
        Exportacion.objects.create(
            idExportacion=request.POST.get('export_id'),
            fechaDeclaracion=request.POST.get('declaration_date'),
            cliente=request.POST.get('client'),
            descripcionMercancia=request.POST.get('description'),
            codigoArancelario=request.POST.get('tariff_code'),
            cantidad=request.POST.get('quantity'),
            unidadMedida=request.POST.get('unit'),
            valorFob=request.POST.get('fob_value'),
            impuestos=request.POST.get('taxes'),
            destinoMercancia=request.POST.get('destiny_country'),
            puertoSalida=request.POST.get('exit_port'),
            transporteID=transporte,
            responsableID=responsable,
        )  
        return redirect('registro_exitoso2')
    return render(request, 'registro_exportacion.html',{'transportes': transportes, 'responsables': responsables})

@require_role('Administrador')
def modificar_exportacion(request):
    exportaciones = Exportacion.objects.all()
    transportes = Transporte.objects.all()
    responsables = Usuario.objects.all()
    exportacion = None  

    export_data = None
    export_id = request.session.get('selected_export_id', None) or request.GET.get('export_id')
    
    if export_id:
        try:
            export_data = Exportacion.objects.get(idExportacion=export_id)
        except Exportacion.DoesNotExist:
            export_data = None
        finally:
            if 'selected_export_id' in request.session:
                del request.session['selected_export_id']
    
    if request.method == 'POST':
        export_id = request.POST.get('export_id')
        if export_id:
            try:
                exportacion = Exportacion.objects.get(idExportacion=export_id)
                
                exportacion.fechaDeclaracion = request.POST.get('declaration_date')
                exportacion.cliente = request.POST.get('client')
                exportacion.descripcionMercancia = request.POST.get('description')
                exportacion.codigoArancelario = request.POST.get('tariff_code')
                exportacion.cantidad = request.POST.get('quantity')
                exportacion.unidadMedida = request.POST.get('unit')
                exportacion.valorFob = request.POST.get('fob_value')
                exportacion.impuestos = request.POST.get('taxes')
                exportacion.destinoMercancia = request.POST.get('destiny_country')
                exportacion.puertoSalida = request.POST.get('exit_port')
                
                transporte_id = request.POST.get('transport_id')
                responsable_id = request.POST.get('responsible_id')
                
                if transporte_id:
                    transporte = get_object_or_404(Transporte, idTransporte=transporte_id)
                    exportacion.transporteID = transporte
                if responsable_id:
                    responsable = get_object_or_404(Usuario, id=responsable_id)
                    exportacion.responsableID = responsable

                exportacion.save()  
                return redirect('modificacion_exitosa')
            except Exportacion.DoesNotExist:
                return render(request, 'modificar_exportacion.html', {
                    'exportaciones': exportaciones,
                    'transportes': transportes,
                    'responsables': responsables,
                    'error': 'Exportación no encontrada.',
                    'export_data': export_data
                })

    if request.method == 'GET':
        export_id = request.GET.get('export_id') 
        if export_id:
            try:
                exportacion = Exportacion.objects.get(idExportacion=export_id)
                return JsonResponse({
                    'declaration_date': exportacion.fechaDeclaracion,
                    'client': exportacion.cliente, 
                    'description': exportacion.descripcionMercancia,
                    'tariff_code': exportacion.codigoArancelario,
                    'quantity': exportacion.cantidad,
                    'unit': exportacion.unidadMedida,
                    'fob_value': exportacion.valorFob,
                    'taxes': exportacion.impuestos,
                    'destiny_country': exportacion.destinoMercancia,
                    'exit_port': exportacion.puertoSalida,
                    'transport_id': exportacion.transporteID.idTransporte if exportacion.transporteID else None,
                    'responsible_id': exportacion.responsableID.id if exportacion.responsableID else None
                })
            except Exportacion.DoesNotExist:
                return JsonResponse({'error': 'No se encontró la exportación.'}, status=404)

    return render(request, 'modificar_exportacion.html', {
        'exportaciones': exportaciones,
        'exportacion': exportacion,
        'transportes': transportes,
        'responsables': responsables,
        'export_data': export_data
    })


@require_role('Administrador')
def consultar_exportacion(request):
    exportaciones = Exportacion.objects.all()
    export_data = None

    export_id = request.GET.get('export_id', None)

    if export_id:
        try:
            export_data = Exportacion.objects.get(idExportacion=export_id)
            request.session['selected_export_id'] = export_id
        except Exportacion.DoesNotExist:
            export_data = None
            if 'selected_export_id' in request.session:
                del request.session['selected_export_id']


    return render(request, 'consultar_exportacion.html', {'exportaciones': exportaciones, 'export_data': export_data})

@require_role('Supervisor')
def consultar_exportacionS(request):
    exportaciones = Exportacion.objects.all()
    expo_data = None

    export_id = request.GET.get('export_id', '').strip()

    if export_id.isdigit():
        try:
            expo_data = Exportacion.objects.get(idExportacion=export_id)
        except Exportacion.DoesNotExist:
            expo_data = None
    else:
        expo_data = None

    return render(request, 'consultar_exportacionS.html', {'exportaciones': exportaciones, 'expo_data': expo_data})


@require_role('Administrador')
def listar_exportaciones(request):
    exportaciones = Exportacion.objects.all()  # Obtén todas las exportaciones
    return render(request, 'listar_exportaciones.html', {'exportaciones': exportaciones})

@require_role('Supervisor')
def listar_exportacionesS(request):
    exportaciones = Exportacion.objects.all()  # Obtén todas las exportaciones
    return render(request, 'listar_exportacionesS.html', {'exportaciones': exportaciones})

@require_role('Administrador')
def eliminar_exportacion(request):
    exportaciones = Exportacion.objects.all()
    eliminado = None  

    if request.method == "POST":
        export_id = request.POST.get("export_id")
        try:
            exportacion = Exportacion.objects.get(idExportacion=export_id)
            
            ExportacionBorrada.objects.create(
                idExportacion=exportacion.idExportacion,
                fechaDeclaracion=exportacion.fechaDeclaracion,
                cliente=exportacion.cliente,
                descripcionMercancia=exportacion.descripcionMercancia,
                codigoArancelario=exportacion.codigoArancelario,
                cantidad=exportacion.cantidad,
                unidadMedida=exportacion.unidadMedida,
                valorFob=exportacion.valorFob,
                impuestos=exportacion.impuestos,
                destinoMercancia=exportacion.destinoMercancia,
                puertoSalida=exportacion.puertoSalida,
                transporteID=exportacion.transporteID,
                responsableID=exportacion.responsableID
            )

            exportacion.delete()
            eliminado = True
        except Exportacion.DoesNotExist:
            eliminado = False

    return render(request, 'eliminar_exportacion.html', {'exportaciones': exportaciones, 'eliminado': eliminado})



@require_role('Administrador')
def registro_transporte(request):
    responsables = Usuario.objects.all()  
    
    if request.method == 'POST':
        id_transporte = request.POST.get('id_transporte')
        empresa_transporte = request.POST.get('empresa_transporte')
        medio_transporte = request.POST.get('medio_transporte')
        numero_matricula = request.POST.get('numero_matricula')
        conductor = request.POST.get('conductor')
        ruta = request.POST.get('ruta')
        fecha_salida = request.POST.get('fecha_salida')
        fecha_llegada = request.POST.get('fecha_llegada')
        estado_transporte = request.POST.get('estado_transporte')
        responsable_id = request.POST.get('responsable_id')
        
        responsable = get_object_or_404(Usuario, id=responsable_id) if responsable_id else None
        
        Transporte.objects.create(
            idTransporte=id_transporte,
            empresaTransporte=empresa_transporte,
            medioTransporte=medio_transporte,
            numeroMatricula=numero_matricula,
            conductor=conductor,
            ruta=ruta,
            fechaSalida=fecha_salida,
            fechaLlegada=fecha_llegada,
            estadoTransporte=estado_transporte,
            responsableID=responsable
        )
        
        return redirect('registro_exitoso2')
    
    return render(request, 'registro_transporte.html', {'responsables': responsables})

@require_role('Administrador')
def listar_transporte(request):
    transportes = Transporte.objects.all()  # Obtén todos los transportes
    return render(request, 'listar_transporte.html', {'transportes': transportes})

@require_role('Supervisor')
def listar_transporteS(request):
    transportes = Transporte.objects.all()  # Obtén todos los transportes
    return render(request, 'listar_transporteS.html', {'transportes': transportes})

@require_role('Administrador')
def modificar_transporte(request):
    transportes = Transporte.objects.all()
    responsables = Usuario.objects.all()
    transporte = None 

    transporte_data = None
    transporte_id = request.session.get('selected_id_transporte', None) or request.GET.get('transporte_id')
    
    if transporte_id:
        try:
            transporte_data = Transporte.objects.get(idTransporte=transporte_id)
        except Transporte.DoesNotExist:
            transporte_data = None
        finally:
            if 'selected_id_transporte' in request.session:
                del request.session['selected_id_transporte']
        
    if request.method == 'POST':
        transporte_id = request.POST.get('transporte_id') 
        if transporte_id:
            try:
                transporte = Transporte.objects.get(idTransporte=transporte_id)
                
                transporte.empresaTransporte = request.POST.get('empresa_transporte')
                transporte.medioTransporte = request.POST.get('medio_transporte')
                transporte.numeroMatricula = request.POST.get('numero_matricula')
                transporte.conductor = request.POST.get('conductor')
                transporte.ruta = request.POST.get('ruta')
                transporte.fechaSalida = request.POST.get('fecha_salida')
                transporte.fechaLlegada = request.POST.get('fecha_llegada')
                transporte.estadoTransporte = request.POST.get('estado_transporte')
                
                responsable_id = request.POST.get('responsable_id')
                if responsable_id:
                    responsable = get_object_or_404(Usuario, id=responsable_id)
                    transporte.responsableID = responsable

                transporte.save() 
                return redirect('modificacion_exitosa') 
            except Transporte.DoesNotExist:
                return render(request, 'modificar_transporte.html', {
                    'transportes': transportes,
                    'responsables': responsables,
                    'error': 'Transporte no encontrado.',
                    'transporte_data': transporte_data
                })

    if request.method == 'GET':
        transporte_id = request.GET.get('transporte_id')
        if transporte_id:
            try:
                transporte = Transporte.objects.get(idTransporte=transporte_id)
                return JsonResponse({
                    'empresa_transporte': transporte.empresaTransporte,
                    'medio_transporte': transporte.medioTransporte,
                    'numero_matricula': transporte.numeroMatricula,
                    'conductor': transporte.conductor,
                    'ruta': transporte.ruta,
                    'fecha_salida': transporte.fechaSalida,
                    'fecha_llegada': transporte.fechaLlegada,
                    'estado_transporte': transporte.estadoTransporte,
                    'responsable_id': transporte.responsableID.id
                })
            except Transporte.DoesNotExist:
                return JsonResponse({'error': 'No se encontró el transporte.'}, status=404)

    return render(request, 'modificar_transporte.html', {
        'transportes': transportes,
        'transporte': transporte,
        'responsables': responsables,
        'transporte_data': transporte_data
    })

@require_role('Administrador')
def consultar_transporte(request):
    transportes = Transporte.objects.all()
    transporte_data = None

    id_transporte = request.GET.get('idTransporte', None)
    if id_transporte:
        try:
            transporte_data = Transporte.objects.get(idTransporte=id_transporte)
            request.session['selected_id_transporte'] = id_transporte
        except Transporte.DoesNotExist:
            transporte_data = None
            if 'selected_id_transporte' in request.session:
                del request.session['selected_id_transporte']

    return render(request, 'consultar_transporte.html', {
        'transportes': transportes,
        'transporte_data': transporte_data
    })


@require_role('Supervisor')
def consultar_transporteS(request):
    transportes = Transporte.objects.all()
    transporte_data = None

    id_transporte = request.GET.get('idTransporte', None)
    if id_transporte:
        try:
            transporte_data = Transporte.objects.get(idTransporte=id_transporte)
        except Transporte.DoesNotExist:
            transporte_data = None

    return render(request, 'consultar_transporteS.html', {
        'transportes': transportes,
        'transporte_data': transporte_data
    })
        

@require_role('Administrador')
def eliminar_transporte(request):
    transportes = Transporte.objects.all()
    eliminado = None  # Variable para verificar si se eliminó correctamente

    if request.method == "POST":
        transporte_id = request.POST.get("transporte_id")
        try:
            transporte = Transporte.objects.get(idTransporte=transporte_id)
            
            # Copiar el registro a la tabla TransporteBorrado
            TransporteBorrado.objects.create(
                idTransporte=transporte.idTransporte,
                empresaTransporte=transporte.empresaTransporte,
                medioTransporte=transporte.medioTransporte,
                numeroMatricula=transporte.numeroMatricula,
                conductor=transporte.conductor,
                ruta=transporte.ruta,
                fechaSalida=transporte.fechaSalida,
                fechaLlegada=transporte.fechaLlegada,
                estadoTransporte=transporte.estadoTransporte,
                responsableID=transporte.responsableID
            )
            
            # Eliminar el registro de la tabla principal
            transporte.delete()
            eliminado = True
        except Transporte.DoesNotExist:
            eliminado = False

    return render(request, 'eliminar_transporte.html', {'transportes': transportes, 'eliminado': eliminado})


@require_role('Administrador')
def registro_control(request):
    responsables = Usuario.objects.all() 
    importaciones = Importacion.objects.all()
    exportaciones = Exportacion.objects.all()
    
    if request.method == 'POST':  
        responsable = get_object_or_404(Usuario, id=request.POST.get('responsible_id'))
        importacion = get_object_or_404(Importacion, idImportacion=request.POST.get('import_id')) if request.POST.get('import_id') else None
        exportacion = get_object_or_404(Exportacion, idExportacion=request.POST.get('export_id')) if request.POST.get('export_id') else None
        
        Control.objects.create(
            idControl=request.POST.get('control_id'),
            fechaInspeccion=request.POST.get('inspection_date'),
            horaInspeccion=request.POST.get('inspection_time'),
            tipoControl=request.POST.get('control_type'),
            resultadoInspeccion=request.POST.get('inspection_result'),
            descripcionHallazgos=request.POST.get('findings_description'),
            idImportacion=importacion,
            idExportacion=exportacion,
            responsableID=responsable,
        )  
        return redirect('registro_exitoso2')  # Redirigir a una página de éxito de registro
    
    return render(request, 'registro_control.html', {
        'responsables': responsables,
        'importaciones': importaciones,
        'exportaciones': exportaciones,
    })

@require_role('Administrador')
def modificar_control(request):
    controles = Control.objects.all()
    responsables = Usuario.objects.all()
    importaciones = Importacion.objects.all()
    exportaciones = Exportacion.objects.all()
    control = None 

    control_data = None
    control_id = request.session.get('selected_idControl', None) or request.GET.get('control_id')
    
    if control_id:
        try:
            control_data = Control.objects.get(idControl=control_id)
        except Control.DoesNotExist:
            control_data: None
        finally:
            if 'selected_idControl' in request.session:
                del request.session['selected_idControl']
                
    if request.method == 'POST':
        control_id = request.POST.get('control_id')
        if control_id:
            try:
                control = Control.objects.get(idControl=control_id)

                control.fechaInspeccion = request.POST.get('inspection_date')
                control.horaInspeccion = request.POST.get('inspection_time')
                control.tipoControl = request.POST.get('control_type')
                control.resultadoInspeccion = request.POST.get('inspection_result')
                control.descripcionHallazgos = request.POST.get('findings_description')

                importacion_id = request.POST.get('import_id')
                if importacion_id:
                    importacion = get_object_or_404(Importacion, idImportacion=importacion_id)
                    control.idImportacion = importacion
                else:
                    control.idImportacion = None

                exportacion_id = request.POST.get('export_id')
                if exportacion_id:
                    exportacion = get_object_or_404(Exportacion, idExportacion=exportacion_id)
                    control.idExportacion = exportacion
                else:
                    control.idExportacion = None

                responsable_id = request.POST.get('responsible_id')
                if responsable_id:
                    responsable = get_object_or_404(Usuario, id=responsable_id)
                    control.responsableID = responsable

                control.save()
                return redirect('modificacion_exitosa')  # 

            except Control.DoesNotExist:
                return render(request, 'modificar_control.html', {
                    'controles': controles,
                    'responsables': responsables,
                    'importaciones': importaciones,
                    'exportaciones': exportaciones,
                    'error': 'Control no encontrado.',
                    'control_data': control_data
                })

    if request.method == 'GET':
        control_id = request.GET.get('control_id')
        if control_id:
            try:
                control = Control.objects.get(idControl=control_id)
                return JsonResponse({
                    'fechaInspeccion': control.fechaInspeccion if control.fechaInspeccion else '',
                    'horaInspeccion': control.horaInspeccion if control.horaInspeccion else '',
                    'tipoControl': control.tipoControl if control.tipoControl else '',
                    'resultadoInspeccion': control.resultadoInspeccion if control.resultadoInspeccion else '',
                    'descripcionHallazgos': control.descripcionHallazgos if control.descripcionHallazgos else '',
                    'idImportacion': control.idImportacion.idImportacion if control.idImportacion else '',
                    'idExportacion': control.idExportacion.idExportacion if control.idExportacion else '',
                    'responsableID': control.responsableID.id if control.responsableID else ''
                })
            except Control.DoesNotExist:
                return JsonResponse({'error': 'No se encontró el control.'}, status=404)



    return render(request, 'modificar_control.html', {
        'controles': controles,
        'control': control,
        'responsables': responsables,
        'importaciones': importaciones,
        'exportaciones': exportaciones,
        'control_data': control_data
    })
    
    
@require_role('Administrador')
def consultar_control(request):
    controles = Control.objects.all()
    control_data = None

    id_control = request.GET.get('idControl', None)

    if id_control:
        try:
            control_data = Control.objects.get(idControl=id_control)
            request.session['selected_idControl'] = id_control
        except Control.DoesNotExist:
            control_data = None
            if 'selected_idControl' in request.session:
                del request.session['selected_idControl']

    return render(request, 'consultar_control.html', {
        'controles': controles,
        'control_data': control_data
    })


@require_role('Supervisor')
def consultar_controlS(request):
    controles = Control.objects.all()
    control_data = None

    id_control = request.GET.get('idControl', '').strip()

    if id_control.isdigit():
        try:
            control_data = Control.objects.get(idControl=id_control)
        except Control.DoesNotExist:
            control_data = None
    else:
        control_data = None

    return render(request, 'consultar_controlS.html', {
        'controles': controles,
        'control_data': control_data
    })
    

@require_role('Administrador')   
def listar_control(request):
    controles = Control.objects.all()  # Obtén todos los controles
    return render(request, 'listar_control.html', {'controles': controles})

@require_role('Supervisor')
def listar_controlS(request):
    controles = Control.objects.all()  # Obtén todos los controles
    return render(request, 'listar_controlS.html', {'controles': controles})

@require_role('Administrador')
def eliminar_control(request):
    controles = Control.objects.all()
    eliminado = None  # Variable para verificar si se eliminó correctamente

    if request.method == "POST":
        control_id = request.POST.get("control_id")
        try:
            control = Control.objects.get(idControl=control_id)
            
            # Copiar el registro a la tabla ControlBorrado
            ControlBorrado.objects.create(
                idControl=control.idControl,
                fechaInspeccion=control.fechaInspeccion,
                horaInspeccion=control.horaInspeccion,
                tipoControl=control.tipoControl,
                resultadoInspeccion=control.resultadoInspeccion,
                descripcionHallazgos=control.descripcionHallazgos,
                idImportacion=control.idImportacion,
                idExportacion=control.idExportacion,
                responsableID=control.responsableID
            )
            
            # Eliminar el registro de la tabla principal
            control.delete()
            eliminado = True
        except Control.DoesNotExist:
            eliminado = False

    return render(request, 'eliminar_control.html', {'controles': controles, 'eliminado': eliminado})

@require_role('Administrador')
def registro_carga(request):
    importaciones = Importacion.objects.all()
    exportaciones = Exportacion.objects.all()
    responsables = Usuario.objects.all()

    if request.method == 'POST':
        # Recuperar los valores del formulario
        importacion = get_object_or_404(Importacion, idImportacion=request.POST.get('import_id')) if request.POST.get('import_id') else None
        exportacion = get_object_or_404(Exportacion, idExportacion=request.POST.get('export_id')) if request.POST.get('export_id') else None
        responsable = get_object_or_404(Usuario, id=request.POST.get('responsible_id'))
        
        # Crear un nuevo registro de carga
        Carga.objects.create(
            idCarga=request.POST.get('carga_id'),
            tipoCarga=request.POST.get('load_type'),
            descripcionCarga=request.POST.get('load_description'),
            pesoBruto=request.POST.get('gross_weight'),
            pesoNeto=request.POST.get('net_weight'),
            volumen=request.POST.get('volume'),
            embalaje=request.POST.get('packaging'),
            contenido=request.POST.get('content'),
            valorDeclarado=request.POST.get('declared_value'),
            seguroCarga=request.POST.get('load_insurance'),
            estadoCarga=request.POST.get('load_status'),
            idImportacion=importacion,
            idExportacion=exportacion,
            responsableID=responsable,
        )
        return redirect('registro_exitoso2')  # Redirige a una página de éxito

    return render(request, 'registro_carga.html', {
        'importaciones': importaciones,
        'exportaciones': exportaciones,
        'responsables': responsables,
    })


@require_role('Administrador')
def modificar_carga(request):
    cargas = Carga.objects.all()
    responsables = Usuario.objects.all()
    importaciones = Importacion.objects.all()
    exportaciones = Exportacion.objects.all()
    carga = None 

    carga_data = None
    carga_id = request.session.get('selected_idCarga', None) or request.GET.get('carga_id')
    
    if carga_id:
        try:
            carga_data = Carga.objects.get(idCarga=carga_id)
        except Carga.DoesNotExist:
            carga_data: None
        finally:
            if 'selected_idCarga' in request.session:
                del request.session['selected_idCarga']

    if request.method == 'POST':
        carga_id = request.POST.get('carga_id')
        if carga_id:
            try:
                carga = Carga.objects.get(idCarga=carga_id)

                carga.tipoCarga = request.POST.get('tipo_carga')
                carga.descripcionCarga = request.POST.get('descripcion_carga')
                carga.pesoBruto = request.POST.get('peso_bruto')
                carga.pesoNeto = request.POST.get('peso_neto')
                carga.volumen = request.POST.get('volumen')
                carga.embalaje = request.POST.get('embalaje')
                carga.contenido = request.POST.get('contenido')
                carga.valorDeclarado = request.POST.get('valor_declarado')
                carga.seguroCarga = request.POST.get('seguro_carga')
                carga.estadoCarga = request.POST.get('estado_carga')

                importacion_id = request.POST.get('id_importacion')
                if importacion_id:
                    importacion = get_object_or_404(Importacion, idImportacion=importacion_id)
                    carga.idImportacion = importacion
                else:
                    carga.idImportacion = None
                    
                exportacion_id = request.POST.get('id_exportacion')
                if exportacion_id:
                    exportacion = get_object_or_404(Exportacion, idExportacion=exportacion_id)
                    carga.idExportacion = exportacion
                else:
                    carga.idExportacion = None
                    
                responsable_id = request.POST.get('responsable_id')
                if responsable_id:
                    responsable = get_object_or_404(Usuario, id=responsable_id)
                    carga.responsableID = responsable

                carga.save()  
                return redirect('modificacion_exitosa')  

            except Carga.DoesNotExist:
                return render(request, 'modificar_carga.html', {
                    'cargas': cargas,
                    'responsables': responsables,
                    'importaciones': importaciones,
                    'exportaciones': exportaciones,
                    'error': 'Carga no encontrada.',
                    'carga_data': carga_data
                })

    if request.method == 'GET':
        carga_id = request.GET.get('carga_id')
        if carga_id:
            try:
                carga = Carga.objects.get(idCarga=carga_id)
                return JsonResponse({
                    'tipoCarga': carga.tipoCarga,
                    'descripcionCarga': carga.descripcionCarga,
                    'pesoBruto': str(carga.pesoBruto),
                    'pesoNeto': str(carga.pesoNeto),
                    'volumen': str(carga.volumen),
                    'embalaje': carga.embalaje,
                    'contenido': carga.contenido,
                    'valorDeclarado': str(carga.valorDeclarado),
                    'seguroCarga': str(carga.seguroCarga),
                    'estadoCarga': carga.estadoCarga,
                    'idImportacion': carga.idImportacion.idImportacion if carga.idImportacion else None,
                    'idExportacion': carga.idExportacion.idExportacion if carga.idExportacion else None,
                    'responsableID': carga.responsableID.id if carga.responsableID else None
                })
            except Carga.DoesNotExist:
                return JsonResponse({'error': 'No se encontró la carga.'}, status=404)

    return render(request, 'modificar_carga.html', {
        'cargas': cargas,
        'carga': carga,
        'responsables': responsables,
        'importaciones': importaciones,
        'exportaciones': exportaciones,
        'carga_data': carga_data
    })


@require_role('Administrador')
def consultar_carga(request):
    cargas = Carga.objects.all() 
    carga_data = None  

    id_carga = request.GET.get('idCarga', None)
    
    if id_carga:
        try:
            carga_data = Carga.objects.get(idCarga=id_carga)
            request.session['selected_idCarga'] = id_carga
        except Carga.DoesNotExist:
            carga_data = None
            if 'selected_idCarga' in request.session:
                del request.session['selected_idCarga']
        
    return render(request, 'consultar_carga.html', {'cargas': cargas, 'carga_data': carga_data})


@require_role('Supervisor')
def consultar_cargaS(request):
    cargas = Carga.objects.all()  
    carga_data = None  

    id_carga = request.GET.get('idCarga', None)
    
    if id_carga:
        try:
            carga_data = Carga.objects.get(idCarga=id_carga)
        except Carga.DoesNotExist:
            carga_data = None
    else:
        carga_data = None
        
    return render(request, 'consultar_cargaS.html', {'cargas': cargas, 'carga_data': carga_data})

@require_role('Administrador')
def listar_carga(request):
    cargas = Carga.objects.all()  # Obtén todas las cargas
    return render(request, 'listar_carga.html', {'cargas': cargas})

@require_role('Supervisor')
def listar_cargaS(request):
    cargas = Carga.objects.all()  # Obtén todas las cargas
    return render(request, 'listar_cargaS.html', {'cargas': cargas})


@require_role('Administrador')
def eliminar_carga(request):
    cargas = Carga.objects.all()
    eliminado = None  

    if request.method == "POST":
        carga_id = request.POST.get("carga_id")
        try:
            carga = Carga.objects.get(idCarga=carga_id)
            
            CargaBorrado.objects.create(
                idCarga=carga.idCarga,
                tipoCarga=carga.tipoCarga,
                descripcionCarga=carga.descripcionCarga,
                pesoBruto=carga.pesoBruto,
                pesoNeto=carga.pesoNeto,
                volumen=carga.volumen,
                embalaje=carga.embalaje,
                contenido=carga.contenido,
                valorDeclarado=carga.valorDeclarado,
                seguroCarga=carga.seguroCarga,
                estadoCarga=carga.estadoCarga,
                idImportacion=carga.idImportacion,
                idExportacion=carga.idExportacion,
                responsableID=carga.responsableID
            )
            
            carga.delete()
            eliminado = True
        except Carga.DoesNotExist:
            eliminado = False

    return render(request, 'eliminar_carga.html', {'cargas': cargas, 'eliminado': eliminado})




###############################################################################################
def listar_usuario_borrado(request):
    usuarios_borrados = UsuarioBorrado.objects.all()
    return render(request, 'listar_borrados.html', {'usuarios_borrados': usuarios_borrados})

def listar_importacion_borrado(request):
    importaciones_borradas = ImportacionBorrada.objects.all()
    return render(request, 'listar_borrados.html', {'importaciones_borradas': importaciones_borradas})

def listar_exportacion_borrado(request):
    exportaciones_borradas = ExportacionBorrada.objects.all()
    return render(request, 'listar_borrados.html', {'exportaciones_borradas': exportaciones_borradas})

def listar_transporte_borrado(request):
    transportes_borrados = TransporteBorrado.objects.all()
    return render(request, 'listar_borrados.html', {'transportes_borrados': transportes_borrados})

def listar_control_borrado(request):
    controles_borrados = ControlBorrado.objects.all()
    return render(request, 'listar_borrados.html', {'controles_borrados': controles_borrados})

def listar_carga_borrado(request):
    cargas_borradas = CargaBorrado.objects.all()
    return render(request, 'listar_borrados.html', {'cargas_borradas': cargas_borradas})

def listar_borrados(request):
    usuarios_borrados = UsuarioBorrado.objects.all()
    importaciones_borradas = ImportacionBorrada.objects.all()
    exportaciones_borradas = ExportacionBorrada.objects.all()
    transportes_borrados = TransporteBorrado.objects.all()
    controles_borrados = ControlBorrado.objects.all()
    cargas_borradas = CargaBorrado.objects.all()
    return render(request, 'listar_borrados.html', {
        'usuarios_borrados': usuarios_borrados,
        'importaciones_borradas': importaciones_borradas,
        'exportaciones_borradas': exportaciones_borradas,
        'transportes_borrados': transportes_borrados,
        'controles_borrados': controles_borrados,
        'cargas_borradas': cargas_borradas,
    })