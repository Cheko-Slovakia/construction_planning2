from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from cpmAPI.models import Test, Trabajador, Cliente, Obra, Material, Avance, InventarioObra
from cpmAPI.serializers import TestSerializer, TrabajadorSerializer, ClienteSerializer, ObraSerializer, \
    MaterialSerializer, AvanceSerializer, InventarioObraSerializer
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from cpmAPI.aux_functions import checkInt


# Create your views here.
@csrf_exempt
def testApi(request, id=0):
    if request.method == 'GET':
        tests = Test.objects.all()
        tests_serializer = TestSerializer(tests, many=True)
        return JsonResponse(tests_serializer.data, safe=False)

    elif request.method == 'POST':
        test_data = JSONParser().parse(request)
        test_serializer = TestSerializer(data=test_data)
        if test_serializer.is_valid():
            test_serializer.save()
            return JsonResponse("Added succesfully", safe=False)
        return JsonResponse("Failed to add.", safe=False)

    elif request.method == 'PUT':
        test_data = JSONParser().parse(request)
        test = Test.objects.get(TestId=test_data['TestId'])
        test_serializer = TestSerializer(test, data=test_data)
        if test_serializer.is_valid():
            test_serializer.save()
            return JsonResponse("Updated Succesfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method == 'DELETE':
        test = Test.objects.get(TestId=id)
        test.delete()
        return JsonResponse("Deleted Succesfully!", safe=False)


@csrf_exempt
def trabajadorAPI(request, id=0, ):
    cargo = str(request.GET.get('cargo')) or None

    if request.method == 'GET':
        if id != 0:
            if checkInt(id):
                try:
                    trabajador = Trabajador.objects.get(numero_cedula=str(id))
                    trabajador_serializer = TrabajadorSerializer(trabajador)
                    return JsonResponse(trabajador_serializer.data, safe=False)
                except ObjectDoesNotExist:
                    return JsonResponse("El trabajador con cedula " + str(id) + " no existe", safe=False)
            else:
                try:
                    trabajador = Trabajador.objects.filter(
                        Q(nombre__icontains=str(id)) | Q(apellido__icontains=str(id)))
                    trabajador_serializer = TrabajadorSerializer(trabajador, many=True)
                    return JsonResponse(trabajador_serializer.data, safe=False)
                except ObjectDoesNotExist:
                    return JsonResponse("El trabajador " + str(id) + " no existe", safe=False)

        elif cargo != 'None':
            trabajadores = Trabajador.objects.filter(Q(cargo=cargo) & Q(is_active=True))
            trabajador_serializer = TrabajadorSerializer(trabajadores, many=True)
            return JsonResponse(trabajador_serializer.data, safe=False)

        else:
            trabajadores = Trabajador.objects.all()
            trabajador_serializer = TrabajadorSerializer(trabajadores, many=True)
            return JsonResponse(trabajador_serializer.data, safe=False)

    elif request.method == 'POST':
        trabajador_data = JSONParser().parse(request)
        print(trabajador_data)
        trabajador_serializer = TrabajadorSerializer(data=trabajador_data)
        if trabajador_serializer.is_valid():
            obj, created = Trabajador.objects.filter(
                Q(numero_cedula=trabajador_serializer.data['numero_cedula'])).get_or_create(trabajador_serializer.data)
            if created:
                return JsonResponse("Trabajador registrado satisfactoriamente", safe=False)
            else:
                return JsonResponse("Este trabajador ya existe en el sistema", safe=False)
        return JsonResponse("Failed to add.", safe=False)

    elif request.method == 'PUT':
        trabajador_data = JSONParser().parse(request)
        trabajador = Trabajador.objects.get(trabajador_id=trabajador_data['trabajador_id'])

        trabajador_serializer = TrabajadorSerializer(trabajador, data=trabajador_data)
        if trabajador_serializer.is_valid():
            trabajador_serializer.save()
            return JsonResponse("Trabajador actualizado satisfactoriamente!!", safe=False)
        return JsonResponse("Failed to Update trabajador.", safe=False)

    elif request.method == 'DELETE':
        trabajador = Trabajador.objects.get(trabajador_id=id)
        trabajador.is_active = 0
        trabajador.save()
        return JsonResponse("Deactivated Succesfully!", safe=False)


@csrf_exempt
def clienteAPI(request, id=0, ):
    if request.method == 'GET':
        all = int(request.GET.get('all') or 0)
        is_active = int(request.GET.get('is_active') or 1)
        numero_nit = str(request.GET.get('numero_nit'))
        nombre = str(request.GET.get('nombre'))
        apellido = str(request.GET.get('apellido'))

        if all == 1:
            clientes = Cliente.objects.filter(Q(is_active=is_active))
            cliente_serializer = ClienteSerializer(clientes, many=True)
            return JsonResponse(cliente_serializer.data, safe=False)

        elif numero_nit != 'None':
            try:
                cliente = Cliente.objects.filter(Q(numero_nit=numero_nit) & Q(is_active=is_active))
                cliente_serializer = ClienteSerializer(cliente, many=True)
                return JsonResponse(cliente_serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse("El cliente con NIT " + nombre + " no existe", safe=False)

        elif nombre != 'None' and apellido != 'None':
            try:
                cliente = Cliente.objects.filter((Q(apellido__icontains=apellido) & Q(nombre__icontains=nombre)),
                                                 Q(is_active=is_active))
                cliente_serializer = ClienteSerializer(cliente, many=True)
                return JsonResponse(cliente_serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse("El cliente con Nombre y apellido" + nombre + " " + apellido + " no existe",
                                    safe=False)

        elif nombre != 'None':
            try:
                cliente = Cliente.objects.filter(Q(nombre__icontains=nombre) & Q(is_active=is_active))
                cliente_serializer = ClienteSerializer(cliente, many=True)
                return JsonResponse(cliente_serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse("El cliente con nombre" + str(id) + " no existe", safe=False)

        elif apellido != 'None':
            try:
                cliente = Cliente.objects.filter(Q(apellido__icontains=apellido) & Q(is_active=is_active))
                cliente_serializer = ClienteSerializer(cliente, many=True)
                return JsonResponse(cliente_serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse("El cliente con apellido" + str(id) + " no existe", safe=False)

    elif request.method == 'POST':
        cliente_data = JSONParser().parse(request)
        print(cliente_data)
        cliente_serializer = ClienteSerializer(data=cliente_data)
        if cliente_serializer.is_valid():
            cliente_serializer.save()
            return JsonResponse("Cliente registrado satisfactoriamente", safe=False)
        else:
            return JsonResponse("Failed to add.", safe=False)

    elif request.method == 'PUT':
        cliente_data = JSONParser().parse(request)
        cliente = Cliente.objects.get(cliente_id=cliente_data['cliente_id'])

        cliente_serializer = ClienteSerializer(cliente, data=cliente_data)
        if cliente_serializer.is_valid():
            cliente_serializer.save()
            return JsonResponse("Cliente actualizado satisfactoriamente!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method == 'DELETE':
        cliente = Cliente.objects.get(cliente_id=id)
        cliente.is_active = 0
        cliente.save()
        return JsonResponse("Deactivated Succesfully!!", safe=False)


@csrf_exempt
def obraAPI(request, id=0, ):
    if request.method == 'GET':
        all = int(request.GET.get('all') or 0)
        fase = int(request.GET.get('fase') or 0)
        obra_id = int(request.GET.get('id') or 0)

        if all == 1:
            obras = Obra.objects.all()
            obra_serializer = ObraSerializer(obras, many=True)
            return JsonResponse(obra_serializer.data, safe=False)
        elif obra_id != 0:
            try:
                obra = Obra.objects.get(obra_id=obra_id)
                obra_serializer = ObraSerializer(obra)
                return JsonResponse(obra_serializer.data)
            except ObjectDoesNotExist:
                return JsonResponse("No hay obras con la id " + str(obra_id), safe=False)

        elif fase != 0:
            try:
                obras = Obra.objects.filter(Q(fase=fase))
                obra_serializer = ClienteSerializer(obras, many=True)
                return JsonResponse(obra_serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse("No hay obras actualmente en fase " + fase, safe=False)

    elif request.method == 'POST':
        obra_data = JSONParser().parse(request)
        obra_data['fase'] = '1'
        print(obra_data)
        obra_serializer = ObraSerializer(data=obra_data)
        if obra_serializer.is_valid(raise_exception=True):
            if not Obra.objects.filter(Q(latitud=obra_data['latitud']) &
                                       Q(longitud=obra_data['longitud'])):
                obra_serializer.save()
                return JsonResponse("Obra registrada satisfactoriamente", safe=False)
            else:
                return JsonResponse("Una obra ya existe en esta longitud y latitud", safe=False)
        else:
            return JsonResponse("Fallo a la hora de registrar la obra, datos invalidos", safe=False)

    elif request.method == 'PUT':
        obra_data = JSONParser().parse(request)
        obra = Obra.objects.get(obra_id=obra_data['obra_id'])

        obra_serializer = ObraSerializer(obra, data=obra_data)
        if obra_serializer.is_valid():
            prueba_igualdad = Obra.objects.get(latitud=obra_data['latitud'], longitud=obra_data['longitud'])
            if Obra.objects.filter(Q(latitud=obra_data['latitud']) &
                                   Q(longitud=obra_data['longitud'])) and \
                    obra == prueba_igualdad:
                obra_serializer.save()
                return JsonResponse("Cliente actualizado satisfactoriamente!!", safe=False)
            else:
                return JsonResponse("Una obra ya existe en esta longitud y latitud", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method == 'DELETE':
        obra = Obra.objects.get(obra_id=id)
        obra.delete()
        return JsonResponse("Obra borrada satisfactoriamente!!", safe=False)


@csrf_exempt
def obraTrabajadorAPI(request, id=0, ):
    obra_id = int(request.GET.get('obra_id') or 0)

    if request.method == 'GET':
        try:
            obra = Obra.objects.get(obra_id=obra_id)
            trabajadores_en_obra = obra.trabajadores_participantes.all()
            trabajadores_serializer = TrabajadorSerializer(trabajadores_en_obra, many=True)
            return JsonResponse(trabajadores_serializer.data, safe=False)
        except ObjectDoesNotExist:
            if obra_id == 0:
                return JsonResponse("Por favor utilice el query parameter ?obra_id= para consultar"
                                    "los clientes asociados a una obra", safe=False)
            else:
                return JsonResponse("La obra que está intentando consultar no existe", safe=False)

    elif request.method == 'POST':
        obra_trabajador_data = JSONParser().parse(request)
        obra = Obra.objects.get(obra_id=obra_trabajador_data['obra_id'])
        trabajador = Trabajador.objects.get(trabajador_id=obra_trabajador_data['trabajador_id'])
        obra.trabajadores_participantes.add(trabajador)
        obra.save()
        return JsonResponse("Trabajador asociado a la obra satisfactoriamente!", safe=False)

    elif request.method == 'DELETE':
        obra = Obra.objects.get(obra_id=obra_id)
        trabajador = obra.trabajadores_participantes.get(trabajador_id=id)
        obra.trabajadores_participantes.remove(trabajador)
        return JsonResponse("Trabajador desvinculado de la obra " + str(obra_id) + " satisfactoriamente", safe=False)


@csrf_exempt
def obraClienteAPI(request, id=0, ):
    obra_id = int(request.GET.get('obra_id') or 0)

    if request.method == 'GET':
        try:
            obra = Obra.objects.get(obra_id=obra_id)
            clientes_en_obra = obra.clientes_participantes.all()
            clientes_serializer = ClienteSerializer(clientes_en_obra, many=True)
            return JsonResponse(clientes_serializer.data, safe=False)
        except ObjectDoesNotExist:
            if obra_id == 0:
                return JsonResponse("Por favor utilice el query parameter ?obra_id= para consultar"
                                    "los clientes asociados a una obra", safe=False)
            else:
                return JsonResponse("La obra que está intentando consultar no existe", safe=False)

    elif request.method == 'POST':
        obra_cliente_data = JSONParser().parse(request)
        obra = Obra.objects.get(obra_id=obra_cliente_data['obra_id'])
        cliente = Cliente.objects.get(cliente_id=obra_cliente_data['cliente_id'])
        obra.clientes_participantes.add(cliente)
        obra.save()
        return JsonResponse("Cliente asociado a la obra satisfactoriamente!", safe=False)

    elif request.method == 'DELETE':
        obra = Obra.objects.get(obra_id=obra_id)
        cliente = obra.clientes_participantes.get(cliente_id=id)
        obra.clientes_participantes.remove(cliente)
        return JsonResponse("Cliente desvinculado de la obra " + str(obra_id) + " satisfactoriamente!", safe=False)


@csrf_exempt
def materialAPI(request, id=0, ):
    material_id = int(request.GET.get('material_id') or 0)

    if request.method == 'GET':
        if material_id == 0:
            materiales = Material.objects.all()
            materiales_serializer = MaterialSerializer(materiales, many=True)
            return JsonResponse(materiales_serializer.data, safe=False)
        else:
            try:
                material = Material.objects.get(material_id=material_id)
                materiales_serializer = MaterialSerializer(material)
                return JsonResponse(materiales_serializer.data, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse("El material con id " + str(material_id) + "no existe", safe=False)

    elif request.method == 'POST':
        material_data = JSONParser().parse(request)
        material_serializer = MaterialSerializer(data=material_data)

        if material_serializer.is_valid(raise_exception=True):
            if not Material.objects.filter(Q(nombre=material_data['nombre'])):
                material_serializer.save()
                return JsonResponse("Material registrado satisfactoriamente", safe=False)
            else:
                return JsonResponse("Este material ya existe en la base de datos", safe=False)

    elif request.method == 'PUT':
        material_data = JSONParser().parse(request)
        material = Material.objects.get(material_id=material_data['material_id'])
        material_serializer = MaterialSerializer(material, data=material_data)
        if material_serializer.is_valid():
            prueba_igualdad = Material.objects.get(nombre=material_data['nombre'])
            if Material.objects.filter(Q(nombre=material_data['nombre'])) and material == prueba_igualdad:
                material_serializer.save()
                return JsonResponse("Material actualizado satisfactoriamente!!", safe=False)
            else:
                return JsonResponse("Un material ya existe con este nombre", safe=False)
        return JsonResponse("Failed to update", safe=False)

    elif request.method == 'DELETE':
        material = Material.objects.get(material_id=id)
        material.delete()
        return JsonResponse("Material borrado satisfactoriamente!!", safe=False)


@csrf_exempt
def avanceAPI(request, id=0, ):
    obra_id = int(request.GET.get('obra_id') or 0)
    aprobado = request.GET.get('aprobado') or None

    if request.method == 'GET':
        if obra_id != 0:
            if aprobado is not None:
                avances = Avance.objects.filter(Q(obra_id=obra_id) & Q(aprobado=aprobado)).select_related('obra')
                avances_serializer = AvanceSerializer(avances, many=True)
                for avance in avances_serializer.data:
                    avance['nombre_obra'] = Obra.objects.get(obra_id=avance['obra']).nombre
                return JsonResponse(avances_serializer.data, safe=False)
            else:
                avances = Avance.objects.filter(Q(obra_id=obra_id))
                avances_serializer = AvanceSerializer(avances, many=True)
                for avance in avances_serializer.data:
                    avance['nombre_obra'] = Obra.objects.get(obra_id=avance['obra']).nombre
                return JsonResponse(avances_serializer.data, safe=False)
        else:
            return JsonResponse("Por favor especifique una obra para"
                                "Extraer los avances con el argumento ?obra_id={int} ", safe=False)

    elif request.method == 'POST':
        avance_data = JSONParser().parse(request)
        avance_serializer = AvanceSerializer(data=avance_data)

        if avance_serializer.is_valid(raise_exception=True):
            avance_serializer.save()
            return JsonResponse("Avance registrado satisfactoriamente", safe=False)
        else:
            return JsonResponse("Datos invalidos para registrar avance", safe=False)

    elif request.method == 'PUT':
        avance_data = JSONParser().parse(request)
        avance = Avance.objects.get(avance_id=avance_data['avance_id'])
        avance_serializer = AvanceSerializer(avance, data=avance_data)
        if avance_serializer.is_valid():
            avance_serializer.save()
            return JsonResponse("Avance actualizado satisfactoriamente!!", safe=False)
        else:
            return JsonResponse("Datos invalidos para actualizar avance", safe=False)

    elif request.method == 'DELETE':
        avance = Avance.objects.get(avance_id=id)
        avance.delete()
        return JsonResponse("Avance borrado satisfactoriamente!!", safe=False)


@csrf_exempt
def obraMaterialesAPI(request, id=0, ):
    obra_id = int(request.GET.get('obra_id') or 0)
    all = int(request.GET.get('all') or 0)
    response = {}

    if request.method == 'GET':
        if obra_id != 0:
            materiales_obra = InventarioObra.objects.filter(Q(obra_id=obra_id)).select_related('obra')
            mateteriales_obra_serializer = InventarioObraSerializer(materiales_obra, many=True)
            for solicitud in mateteriales_obra_serializer.data:
                solicitud['nombre_obra'] = Obra.objects.get(obra_id=solicitud['obra']).nombre
                solicitud['nombre_material'] = Material.objects.get(material_id=solicitud['material']).nombre
            response['code'] = 200
            response['data'] = mateteriales_obra_serializer.data
            return JsonResponse(response, safe=False)
        elif all != 0:
            materiales_obra_sin_aprobar = InventarioObra.objects.filter(Q(aprobado=0))
            mateteriales_obra_serializer = InventarioObraSerializer(materiales_obra_sin_aprobar, many=True)
            for solicitud in mateteriales_obra_serializer.data:
                solicitud['nombre_obra'] = Obra.objects.get(obra_id=solicitud['obra']).nombre
                solicitud['nombre_material'] = Material.objects.get(material_id=solicitud['material']).nombre
            response['code'] = 200
            response['data'] = mateteriales_obra_serializer.data
            return JsonResponse(response, safe=False)
        else:
            response['code'] = 500
            response['data'] = "Por favor especifique una obra para" \
                               " extraer su inventario con el argumento ?obra_id={int} "
            return JsonResponse(response, safe=False)

    elif request.method == 'POST':
        obra_material_data = JSONParser().parse(request)
        obra_material_serializer = InventarioObraSerializer(data=obra_material_data)
        if obra_material_serializer.is_valid(raise_exception=True):
            stock_principal = Material.objects.get(material_id=obra_material_data['material'])
            if stock_principal.cantidad - obra_material_data['cantidad'] >= 0:
                if stock_principal.estado == 'DISPONIBLE':
                    obra_material_serializer.save()
                    stock_principal.cantidad = stock_principal.cantidad - obra_material_data['cantidad']
                    stock_principal.save()

                    response['code'] = 200
                    response['data'] =  str(obra_material_data['cantidad']) + " unidades  de " + stock_principal.nombre + \
                                         " sacadas del inventario principal y añadidas al inventario de la obra"
                    return JsonResponse(response, safe=False)
                else:
                    response['code'] = 500
                    response['data'] = "El material especificado no se encuentra DISPONIBLE"
                    return JsonResponse(response, safe=False)
            else:
                response['code'] = 500
                response['data'] = "Está intentando solicitar " + str(obra_material_data['cantidad']) + " " + stock_principal.nombre +\
                                   " pero actualmente solo hay " + str(stock_principal.cantidad)
                return JsonResponse(response, safe=False)
        else:
            response['code'] = 500
            response['data'] = "Datos invalidos para registrar este material en el inventario"
            return JsonResponse(response, safe=False)

    elif request.method == 'PUT':
        obra_material_data = JSONParser().parse(request)
        obra_material = InventarioObra.objects.get(id=obra_material_data['id'])
        cantidad_original = obra_material.cantidad
        cantidad_nueva = obra_material_data['cantidad']
        delta = cantidad_nueva - cantidad_original
        obra_material_serializer = InventarioObraSerializer(obra_material, data=obra_material_data)
        if obra_material_serializer.is_valid():
            stock_principal = Material.objects.get(material_id=obra_material_data['material'])
            if delta > 0:
                if stock_principal.cantidad - delta > 0:
                    obra_material_serializer.save()
                    response['code'] = 200
                    response['data'] = "Material añadido al inventario satisfactoriamente!!"
                    return JsonResponse(response, safe=False)
                else:
                    response['code'] = 500
                    response['data'] = "Está intentando solicitar " + str(delta) + " " + stock_principal.nombre +\
                                        " extra pero actualmente solo hay " + str(stock_principal.cantidad)
                    return JsonResponse(response, safe=False)
            else:
                obra_material_serializer.save()
                response['code'] = 200
                response['data'] = "Material retirado del inventario satisfactoriamente!!"
                return JsonResponse(response, safe=False)
        else:
            response['code'] = 500
            response['data'] = "Datos invalidos para el inventario de la obra"
            return JsonResponse(response, safe=False)

    elif request.method == 'DELETE':
        obra_material = InventarioObra.objects.get(id=id)
        obra_material.delete()
        return JsonResponse("Material actualizado en el inventario satisfactoriamente", safe=False)


@csrf_exempt
def validacionObrasAPI(request, id=0, ):
    obra_id = int(request.GET.get('obra_id') or 0)
    fase = int(request.GET.get('fase') or 0)

    if request.method == 'GET':
        if obra_id != 0:
            if fase != 0:
                ready_for_next_phase = True
                avances = Avance.objects.filter(Q(obra_id=obra_id) & Q(fase=str(fase)))
                avances_serializer = AvanceSerializer(avances, many=True)
                for avance in avances_serializer.data:
                    if avance['aprobado'] == False:
                        ready_for_next_phase = False

                if len(avances_serializer.data) == 0:
                    return JsonResponse("No hay avances para esta fase de la obra", safe=False)

                return JsonResponse(ready_for_next_phase, safe=False)
            else:
                return JsonResponse("Por favor especifique una fase de obra para"
                                    " validar si sus avances ya fueron aprobados con el argumento ?obra_id={int} ",
                                    safe=False)
        else:
            return JsonResponse("Por favor especifique una obra para"
                                " extraer su inventario con el argumento ?obra_id={int} ", safe=False)
    elif request.method == 'PUT':
        obra_validacion_data = JSONParser().parse(request)
        obra = Obra.objects.get(obra_id=obra_validacion_data['obra_id'])
        obra.fase = str(int(obra.fase) + obra_validacion_data['delta'])
        obra.save()
        return JsonResponse("Fase de obra actualizada correctamente", safe=False)

@csrf_exempt
def validacionSolicitudesAPI(request, id=0, ):
    obra_id = int(request.GET.get('obra_id') or 0)

    if request.method == 'GET':
        if obra_id != 0:
            ready_for_next_phase = True
            solicitudes = InventarioObra.objects.filter(Q(obra_id=obra_id))
            solicitudes_serializer = InventarioObraSerializer(solicitudes, many=True)
            for solicitud in solicitudes_serializer.data:
                if solicitud['aprobado'] == False:
                    ready_for_next_phase = False

            if len(solicitudes_serializer.data) == 0:
                return JsonResponse("No hay solicitudes de material para esta obra", safe=False)

            return JsonResponse(ready_for_next_phase, safe=False)
        else:
            return JsonResponse("Por favor especifique una obra para"
                                " extraer su inventario con el argumento ?obra_id={int} ", safe=False)


@csrf_exempt
def SaveFile(request):
    file = request.FILES['uploadedFile']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)
