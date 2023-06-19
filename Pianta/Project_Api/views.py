# Actualizado por:
# Juan Sebastian Girardot Antonio
# 06/18/2023

from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Project_Api.models import Devices, Project, Template, DatosSensores, SharedProject, graphics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.urls import reverse
from Project_Api.serializers import  DevicesSerializer, ProjectSerializer, TemplateSerializer, ShareProjectSerializer, DatosSensoresSerializer, SharedRelationSerializer, GraphicsSerializer#, SharedProjectValidationSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied
from django.views.generic.base import View
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import uuid
from django.http import Http404


# class SharedrandonView(View):
#     serializer_class = SharedProjectValidationSerializer
    
#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class()
#         return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.POST)
#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             idrandom = validated_data.get('idrandom')
#             return redirect('Project_detail_share', idrandom=idrandom)
#         else:
#             return JsonResponsdsdsadasde(serializer.errors, status=400)


# Definimos la clase ShareProjectView
class ShareProjectView(generics.CreateAPIView):
    # Especificamos que cualquier usuario tiene permiso para acceder a esta vista
    permission_classes = (AllowAny,)
    # Especificamos el serializador que se utilizará para la creación de objetos
    serializer_class = ShareProjectSerializer
    # Especificamos el conjunto de datos sobre los que se realizarán las operaciones
    queryset = SharedProject.objects.all()

    # Definimos un método GET para obtener los proyectos compartidos de un usuario
    def get(self, request, *args, **kwargs):
        # Filtramos los proyectos compartidos por el usuario actual
        shared_projects = SharedProject.objects.filter(user=request.user)
        # Obtenemos una lista de los proyectos asociados a los proyectos compartidos
        projects = [sp.project for sp in shared_projects]
        # Serializamos la lista de proyectos utilizando el serializador ProjectSerializer
        project_serializer = ProjectSerializer(projects, many=True)
        #shared_relation_serializer = SharedRelationSerializer(SharedProject.objects.filter(user=user), many=True)
        data = {
            'projects': project_serializer.data,
            #'shared_relations': shared_relation_serializer.data
        }
        return Response(data)
    def create(self, request, *args, **kwargs):
        # Creamos una instancia del serializador utilizando los datos recibidos en la solicitud
        serializer = self.serializer_class(data=request.data)

        # Verificamos si los datos del serializador son válidos
        if serializer.is_valid():
            # Obtenemos el valor del campo 'idrandom' validado por el serializador
            idrandom = serializer.validated_data['idrandom']

            # Verificamos si el valor de 'idrandom' es un UUID válido
            try:
                uuid.UUID(idrandom)
            except ValueError:
                return Response({"res": "idrandom is not a valid idrandom"}, status=status.HTTP_400_BAD_REQUEST)

            # Intentamos obtener el proyecto con el 'idrandom' proporcionado
            try:
                project = Project.objects.get(idrandom=idrandom)
            except Project.DoesNotExist:
                return Response({"res": "Object with project id does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Verificamos si el proyecto ya ha sido compartido por el usuario
            if SharedProject.objects.filter(user=request.user, project=project).exists():
                return Response({"res": "This project has already been shared by the user"}, status=status.HTTP_400_BAD_REQUEST)

            # Verificamos si el proyecto fue creado por el usuario actual
            if project.relationUserProject == request.user:
                return Response({"res": "You cannot share a project created by yourself"}, status=status.HTTP_400_BAD_REQUEST)

            # Serializamos el proyecto encontrado
            project_serializer = ProjectSerializer(project)

            # Guardamos el proyecto compartido en la cuenta del usuario
            shared_project = SharedProject(user=request.user, project=project)
            shared_project.save()

            # Devolvemos los datos del proyecto serializado como respuesta exitosa
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            # Si los datos del serializador no son válidos, devolvemos los errores como respuesta
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class SharedProjectView(generics.RetrieveAPIView):
    # Especificamos que cualquier usuario tiene permiso para acceder a esta vista
    permission_classes = (AllowAny,)
    # Especificamos el serializador que se utilizará para la respuesta
    serializer_class = ProjectSerializer

    def get(self, request, idrandom=None, format=None):
        # Verificamos si se proporcionó un idrandom
        if idrandom:
            try:
                # Verificamos si idrandom es un UUID válido
                uuid.UUID(idrandom)
            except ValueError:
                # Devolvemos una respuesta personalizada si idrandom no es un UUID válido
                return Response({"res": "Invalid project ID"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Intentamos obtener el proyecto con el idrandom proporcionado
                project = Project.objects.get(idrandom=idrandom)
                # Serializamos el proyecto utilizando el serializador definido
                serializer = self.get_serializer(project)
                # Devolvemos los datos del proyecto serializado como respuesta exitosa
                return Response(serializer.data)
            except Project.DoesNotExist:
                # Si no se encuentra el proyecto, devolvemos una respuesta con un mensaje de error
                return Response({"res": "Object with project id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Si no se proporciona un idrandom, devolvemos una respuesta con un mensaje de error
            return Response({"res": "Object with project id does not exist"}, status=status.HTTP_404_NOT_FOUND)

# Definimos la clase DeleteSharedProjectView
class DeleteSharedProjectView(generics.DestroyAPIView):
    # Especificamos que cualquier usuario tiene permiso para acceder a esta vista
    permission_classes = (AllowAny,)
    # Especificamos el serializador que se utilizará para la operación de eliminación
    serializer_class = ShareProjectSerializer
    # Especificamos el conjunto de datos sobre los que se realizará la operación de eliminación
    queryset = SharedProject.objects.all()

    def get_object(self):
        # Obtener el ID de la relación de la URL
        pk = self.kwargs.get('pk')
        try:
            # Obtener la relación de la base de datos
            shared_project = SharedProject.objects.get(pk=pk)
        except SharedProject.DoesNotExist:
            raise Http404
        # Verificar que la relación pertenece al usuario que realiza la solicitud
        if shared_project.user != self.request.user:
            raise PermissionDenied
        return shared_project

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Definimos la clase SharedProjectList
class SharedProjectList(generics.ListAPIView):
    # Especificamos que solo los usuarios autenticados tienen permiso para acceder a esta vista
    permission_classes = (IsAuthenticated,)
    # Especificamos el conjunto de datos sobre los que se realizará la operación de listado
    queryset = SharedProject.objects.all()
    # Especificamos el serializador que se utilizará para serializar los datos de respuesta
    serializer_class = SharedRelationSerializer
    
    def get_queryset(self):
        # Obtenemos el usuario autenticado
        user = self.request.user
        # Filtramos solo las relaciones del usuario autenticado
        queryset = SharedProject.objects.filter(user=user)
        return queryset

class ProjectListApiView(generics.ListCreateAPIView):
    # Clase de vista API que permite listar y crear proyectos

    permission_classes = (IsAuthenticated, )
    # Se especifica que se requiere autenticación para acceder a esta vista

    queryset = Project.objects.all()
    # Se define el conjunto de datos de proyecto como todos los objetos de la clase Project

    serializer_class = ProjectSerializer
    # Se especifica la clase de serializador a utilizar para serializar/deserializar los datos de proyecto

    def get_queryset(self):
        # Método que devuelve el conjunto de datos filtrado para el usuario que realiza la solicitud
        return Project.objects.filter(relationUserProject=self.request.user)

    def perform_create(self, serializer):
        # Método que se ejecuta al crear un nuevo proyecto
        serializer.save(relationUserProject=self.request.user)

    def get(self, request, *args, **kwargs):
        '''
        Método para obtener una lista de todos los proyectos para el usuario solicitado
        '''
        project = Project.objects.filter(relationUserProject=request.user)
        # Filtrar los proyectos por el usuario que realiza la solicitud
        serializer = ProjectSerializer(project, many=True)
        # Serializar los proyectos en formato adecuado para la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)
        # Devolver los datos serializados como respuesta con estado HTTP 200 OK

    def post(self, request, *args, **kwargs):
        '''
        Create a new project with the given data
        '''
        # Extraer los datos necesarios del cuerpo de la solicitud
        data = {
            'idrandom': request.data.get('idrandom'),
            'name': request.data.get('name'),
            'location': request.data.get('location'),
            'description': request.data.get('description')
        }
        # Obtener el serializador apropiado y validar los datos
        serializer = self.get_serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Crear el nuevo proyecto
        self.perform_create(serializer)
        # Obtener las cabeceras de éxito para la respuesta
        headers = self.get_success_headers(serializer.data)
        # Devolver los datos del proyecto creado como respuesta con estado HTTP 201 Created
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
class ProjectDetailApiView(APIView):
    #Método auxiliar para obtener el objecto con project_id dado
       
    def get_object(self, project_id):
        try:
            return Project.objects.get(id=project_id, relationUserProject=self.request.user)
        except Project.DoesNotExist:
            return None
    #Recupera el elemento Project con project_id dado
    def get(self, request, project_id, *args, **kwargs):
        project_instance = self.get_object(project_id)
        if not project_instance:
            return Response(
                {"res": "Object with project id does not exists"},
                status=status.HTTP_400_BAD_REQUEST    
            )
        serializer = ProjectSerializer(project_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    #Actualiza el elemento Project con project_id dado, si existe
    def put(self, request, project_id, *args, **kwargs):
        project_instance = self.get_object(project_id)
        if not project_instance:
            return Response(
                {"res": "Object with project id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data ={
            'idrandom': request.data.get('idrandom'), # Obtiene el valor de 'idrandom' del objeto 'request.data'
            'name' : request.data.get('name'), # Obtiene el valor de 'name' del objeto 'request.data'
            'location': request.data.get('location'), # Obtiene el valor de 'location' del objeto 'request.data'
            'description' : request.data.get('description'), # Obtiene el valor de 'description' del objeto 'request.data'
        }
        # Crea una instancia del serializador 'ProjectSerializer'
        serializer = ProjectSerializer(
            instance = project_instance, # Asigna la instancia del proyecto existente
            data=data,  # Asigna los datos del proyecto a actualizar
            partial = True # Permite actualizaciones parciales (no se requieren todos los campos)
        )
        if serializer.is_valid(): # Verifica si los datos proporcionados son válidos
            serializer.save()  # Guarda los datos actualizados en la base de datos
            return Response(serializer.data, status=status.HTTP_200_OK) # Devuelve una respuesta con los datos actualizados y el estado HTTP 200 OK
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # Devuelve una respuesta con los errores de validación y el estado HTTP 400 BAD REQUEST si los datos no son válidos
    #Elimina el elemento Project con project_id dado, si existe
    def delete(self, request, project_id, *args, **kwargs):
        project_instance = self.get_object(project_id)# Obtiene la instancia del proyecto con el project_id proporcionado
        if not project_instance:
            return Response(
                {"res": "Object with project id does not exists"}, # Devuelve una respuesta indicando que el objeto con el project_id no existe
                status=status.HTTP_400_BAD_REQUEST # Estado HTTP 400 BAD REQUEST
            )
        project_instance.delete() # Elimina la instancia del proyecto de la base de datos
        return Response(
            {"res": "Object deleted!"},  # Devuelve una respuesta indicando que el objeto ha sido eliminado exitosamente
            status=status.HTTP_200_OK # Estado HTTP 200 OK
        )   


class DevicesListApiView(generics.ListCreateAPIView):
    queryset = Devices.objects.all()
    serializer_class = DevicesSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Devices.objects.filter(relationProject_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            raise ValidationError("Project with the provided ID does not exist.")
        serializer.save(relationProject=project)

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        data = {
            'name': request.data.get('name'),
            'location': request.data.get('location'),
            'relationProject': project_id,
        }
        serializer = DevicesSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DevicesDetailApiView(APIView):
    #Método auxiliar para obtener el objecto con project_id dado
    def get_object(self, device_id):
        try:   # Obtener el ID del proyecto desde los argumentos de la URL
            project_id = self.kwargs['project_id']
            project = Project.objects.get(id=project_id)
            print(project)
            return Devices.objects.get(id=device_id, relationProject_id=project_id)  # Obtiene un objeto Devices con el ID y la relaciónUserDevice específicos
        except Devices.DoesNotExist:
            return None   # Si no se encuentra el objeto, devuelve None (ningún objeto encontrado)

    #Recupera el elemento Project con project_id dado
    def get(self, request, device_id, *args, **kwargs):
        device_instance = self.get_object(device_id)
        if not device_instance:
            return Response({"res": "Object with device id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DevicesSerializer(device_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    #Actualiza el elemento Project con project_id dado, si existe
     # Obtener la instancia del dispositivo basada en el ID proporcionado
    def put(self, request, device_id, *args, **kwargs):
        project_id = self.kwargs['project_id']
        device_instance = self.get_object(device_id)
        if not device_instance:
            return Response({"res": "Object with device id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'name': request.data.get('name'),
            'location': request.data.get('location'),
            'relationProject': project_id,
        }
        serializer = DevicesSerializer(instance=device_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, device_id, *args, **kwargs):
        device_instance = self.get_object(device_id)
        if not device_instance:
            return Response({"res": "Object with device id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        device_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
   

class TemplateListApiView(APIView):
    permission_classes = (IsAuthenticated, )  # Clases de permisos requeridas para acceder a la vista
    queryset = Template.objects.all()  # Conjunto de consultas para obtener todas las instancias de Template
    serializer_class = TemplateSerializer  # Clase de serializador utilizada para serializar/deserializar instancias de Template

    def get_queryset(self):
        # Retorna el conjunto de consultas para obtener todas las instancias de Template relacionadas con el usuario de la solicitud
        return Template.objects.filter(relationUserTemplate=self.request.user)

    def perform_create(self, serializer):
        # Guarda la instancia del Template con la relación establecida al usuario de la solicitud
        serializer.save(relationUserTemplate=self.request.user)

    def get(self, request, *args, **kwargs):
        '''
        Obtiene y devuelve todas las instancias de Template relacionadas con el usuario de la solicitud
        '''
        template = Template.objects.filter(relationUserTemplate=request.user)  # Obtiene todas las instancias de Template relacionadas con el usuario de la solicitud
        serializer = TemplateSerializer(template, many=True)  # Serializa las instancias de Template obtenidas
        return Response(serializer.data, status=status.HTTP_200_OK)  # Devuelve los datos serializados en una respuesta exitosa

    # Lista todos los registros

    # Crea un nuevo registro
    def post(self, request, *args, **kwargs):
        '''
        Crea un nuevo proyecto con los datos proporcionados
        '''
        data = {
            'id': request.data.get('id'),  # Obtén el valor del campo 'id' de la solicitud
            'name': request.data.get('name'),  # Obtén el valor del campo 'name' de la solicitud
            'sensor': request.data.get('sensor'),  # Obtén el valor del campo 'sensor' de la solicitud
            'red' : request.data.get('red'),  # Obtén el valor del campo 'red' de la solicitud
            'descripcion': request.data.get('descripcion'),  # Obtén el valor del campo 'descripcion' de la solicitud
        }
        serializer = TemplateSerializer(data=data, context={'request': request})  # Crea una instancia del serializador con los datos y el contexto proporcionados
        if serializer.is_valid():
            # Si los datos son válidos según las reglas definidas en el serializador, guarda el proyecto y devuelve una respuesta exitosa
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Si los datos no son válidos, devuelve los errores de validación en una respuesta de error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetailApiView(APIView):
    # Método auxiliar para obtener el objeto con project_id dado
    def get_object(self, template_id):
        try:
            # Intenta obtener una instancia de Template con el ID proporcionado
            return Template.objects.get(id=template_id)
        except Template.DoesNotExist:
            # Si no se encuentra ninguna instancia, devuelve None
            return None

    # Recupera el elemento Project con project_id dado
    def get(self, request, template_id, *args, **kwargs):
    # Obtener la instancia de Template basada en el ID proporcionado
        template_instance = self.get_object(template_id)
        
        # Comprobar si la instancia de Template existe
        if not template_instance:
            return Response(
                {"res": "Object with template id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Serializar la instancia de Template
        serializer = TemplateSerializer(template_instance)
        
        # Devolver los datos serializados en una respuesta exitosa
        return Response(serializer.data, status=status.HTTP_200_OK)


    # Actualiza el elemento Project con project_id dado, si existe
    def put(self, request, template_id, *args, **kwargs):
        # Obtener la instancia de Template basada en el ID proporcionado
        template_instance = self.get_object(template_id)
        
        # Comprobar si la instancia de Template existe
        if not template_instance:
            return Response(
                {"res": "Object with template id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'id': request.data.get('id'),  # Obtén el valor del campo 'id' de la solicitud
            'name': request.data.get('name'),  # Obtén el valor del campo 'name' de la solicitud
            'sensor': request.data.get('sensor'),  # Obtén el valor del campo 'sensor' de la solicitud
            'red': request.data.get('red'),  # Obtén el valor del campo 'red' de la solicitud
            'descripcion': request.data.get('descripcion'),  # Obtén el valor del campo 'descripcion' de la solicitud
        }
        
        serializer = TemplateSerializer(
            instance=template_instance,
            data=data,
            partial=True
        )
        
        if serializer.is_valid():
            # Si los datos son válidos según las reglas definidas en el serializador, guarda los cambios y devuelve una respuesta exitosa
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Si los datos no son válidos, devuelve los errores de validación en una respuesta de error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Elimina el elemento Project con project_id dado, si existe
    def delete(self, request, template_id, *args, **kwargs):
        # Obtener la instancia de Template basada en el ID proporcionado
        template_instance = self.get_object(template_id)
        
        # Comprobar si la instancia de Template existe
        if not template_instance:
            return Response(
                {"res": "Object with template id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eliminar la instancia de Template
        template_instance.delete()
        
        # Devolver una respuesta exitosa indicando que el objeto ha sido eliminado
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


# Create your views here.
@csrf_exempt
def save_DatosSensores(request):
    if request.method == 'POST':
        # Obtener los datos de la solicitud POST en formato JSON
        data = request.body.decode('utf-8')
        # Convertir los datos de JSON a un diccionario de Python
        data_dict = json.loads(data)
        # Obtener los valores de los sensores del diccionario
        namePerson = data_dict.get('name', '')
        sensor1_value = data_dict.get('v1', 0)
        sensor2_value = data_dict.get('v2', 0)
        sensor3_value = data_dict.get('v3', 0)
        sensor4_value = data_dict.get('v4', 0)
        sensor5_value = data_dict.get('v5', 0)
        sensor6_value = data_dict.get('v6', 0)
        sensor7_value = data_dict.get('v7', 0)
        sensor8_value = data_dict.get('v8', 0)
        sensor9_value = data_dict.get('v9', 0)
        sensor10_value = data_dict.get('v10', 0)
        sensor11_value = data_dict.get('v11', 0)
        sensor12_value = data_dict.get('v12', 0)
        # Guardar los valores de los sensores en la base de datos
        datos_sensores = DatosSensores(v1=sensor1_value, v2=sensor2_value,v3=sensor3_value,v4=sensor4_value,v5=sensor5_value,v6=sensor6_value,v7=sensor7_value,v8=sensor8_value,v9=sensor9_value,v10=sensor10_value,v11=sensor11_value,v12=sensor12_value,name=namePerson )
        datos_sensores.save()
        # Devolver una respuesta exitosa
        response_data = {'status': 'success'}
        return JsonResponse(response_data)
    
    # Devolver una respuesta de error si la solicitud no es POST
    response_data = {'status': 'error', 'message': 'Metodo no permitido'}
    return JsonResponse(response_data, status=405)

@api_view(['GET'])
def obtener_datos_sensores(request):
    # Obtiene todos los datos de los sensores
    datos_sensores = DatosSensores.objects.values()
    
    # Serializa los datos de los sensores
    serializer = DatosSensoresSerializer(datos_sensores, many=True)
    
    # Devuelve los datos serializados en una respuesta
    return Response(serializer.data)

@api_view(['GET'])
def datos_sensores(request, field):
    # Obtiene los datos de los sensores solo para el campo específico proporcionado
    datos_sensores = DatosSensores.objects.values('name', 'created_at', field)
    
    # Serializa los datos de los sensores
    serializer = DatosSensoresSerializer(datos_sensores, many=True)
    
    # Devuelve los datos serializados en una respuesta
    return Response(serializer.data)

#Graphics
class GraphicsApiView(APIView):
    #permission_classes = (IsAuthenticated, ) 
    queryset = graphics.objects.all()
    serializer_class = GraphicsSerializer

    def get_queryset(self, **kwargs):
        template_id = self.kwargs['id']
        print(template_id)
        return graphics.objects.filter(relationTemplateGraphics_id=template_id)

    def perform_create(self, serializer, **kwargs):
        template_id = self.kwargs['id']
        try:
            template = Template.objects.get(id=template_id)
        except ObjectDoesNotExist:
            # Manejar el caso cuando no se encuentra ninguna instancia de Template
            raise ValidationError("Template with the provided ID does not exist.")
        serializer.save(relationTemplateGraphics=template)

    def get(self, request, *args, **kwargs):
        template_id = self.kwargs['id']
        try:
            template = Template.objects.get(id=template_id)
        except ObjectDoesNotExist:
            # Manejar el caso cuando no se encuentra ninguna instancia de Template
            return Response("Template with the provided ID does not exist.", status=status.HTTP_404_NOT_FOUND)
        graphics_queryset = self.get_queryset().filter(relationTemplateGraphics_id=template_id)
        serializer = GraphicsSerializer(graphics_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        template_id = self.kwargs['id']
        # Obtener los datos del cuerpo de la solicitud
        data = {
            'titlegraphics': request.data.get('titlegraphics'),
            'namegraphics': request.data.get('namegraphics'),
            'aliasgraphics': request.data.get('aliasgraphics'),
            'location': request.data.get('location'),
            'color': request.data.get('color'),
            'is_circular': request.data.get('is_circular', False),
            'relationTemplateGraphics_id': template_id,  # Agregar el ID de la plantilla al diccionario de datos
        }
        # Crear un serializador con los datos de la solicitud y el contexto de la solicitud
        serializer = GraphicsSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Llamar al método perform_create para guardar el gráfico y establecer la relación con la plantilla
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GraphicsApiDetailView(APIView):
    def get_object(self, graphics_id):
        try:
            # Obtener el objeto graphics con el ID proporcionado
            return graphics.objects.get(id=graphics_id)
        except graphics.DoesNotExist:
            # Si no se encuentra el objeto, retornar None
            return None


    # Recupera el elemento Project con project_id dado
    def get(self, request, graphics_id, *args, **kwargs):
        # Obtener la instancia de graphics utilizando el ID proporcionado
        graphics_instance = self.get_object(graphics_id)
        if not graphics_instance:
            # Si no se encuentra la instancia, devolver una respuesta de error
            return Response(
                {"res": "Object with graphics id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Serializar la instancia y devolver una respuesta exitosa
        serializer = GraphicsSerializer(graphics_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # Actualiza el elemento Project con project_id dado, si existe
    def put(self, request, graphics_id, *args, **kwargs):
        # Obtener la instancia de gráficos correspondiente al ID proporcionado
        graphics_instance = self.get_object(graphics_id)
        if not graphics_instance:
            # Si no se encuentra una instancia de gráficos, devolver un error 400
            return Response(
                {"res": "Object with graphics id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener los datos proporcionados en la solicitud
        data = {
            'titlegraphics': request.data.get('titlegraphics', graphics_instance.titlegraphics),
            'namegraphics': request.data.get('namegraphics', graphics_instance.namegraphics),
            'aliasgraphics': request.data.get('aliasgraphics', graphics_instance.aliasgraphics),
            'color': request.data.get('color', graphics_instance.color),
        }
        
        # Crear una instancia del serializador de gráficos con la instancia existente y los datos proporcionados
        serializer = GraphicsSerializer(
            instance=graphics_instance,
            data=data,
            partial=True
        )
        
        if serializer.is_valid():
            # Si los datos son válidos, guardar los cambios en la instancia existente
            serializer.save()
            # Devolver los datos serializados actualizados con un código de estado 200
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Si los datos no son válidos, devolver los errores del serializador con un código de estado 400
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Elimina el elemento Project con project_id dado, si existe
    def delete(self, request, graphics_id, *args, **kwargs):
        # Obtener la instancia de gráficos correspondiente al ID proporcionado
        graphics_instance = self.get_object(graphics_id)
        if not graphics_instance:
            # Si no se encuentra una instancia de gráficos, devolver un error 400
            return Response(
                {"res": "Object with template id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eliminar la instancia de gráficos
        graphics_instance.delete()
        
        # Devolver una respuesta indicando que el objeto ha sido eliminado con éxito
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
