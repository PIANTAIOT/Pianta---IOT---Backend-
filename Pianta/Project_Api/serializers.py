# Actualizado por:
# Yeimmy Katherin Lugo 
# 07/06/2023


from rest_framework import serializers
from .models import Devices, Project, Template, DatosSensores, SharedProject, graphics



# class SharedProjectValidationSerializer(serializers.Serializer):
#     idrandom = serializers.CharField()

#     def validate_idrandom(self, value):
#         try:
#             project = Project.objects.get(idrandom=value)
#         except Project.DoesNotExist:
#             raise serializers.ValidationError("Invalid idrandom")
#         return value

class SharedRelationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # Campo de solo lectura para el ID

    class Meta:
        model = SharedProject
        fields = ['id', 'user', 'project', 'timestamp']
        # Define los campos que se serializarán/deserializarán y se incluirán en la representación del objeto

        
class ShareProjectSerializer(serializers.Serializer):
    idrandom = serializers.CharField(max_length=300)  # Campo de cadena de caracteres con una longitud máxima de 300 caracteres
    # Define el campo "idrandom" que se serializará/deserializará

        
class ProjectSerializer(serializers.ModelSerializer):
    relationUserProject = serializers.ReadOnlyField(source='relationUserProject.username')
    # Define un campo de solo lectura "relationUserProject" que obtiene el nombre de usuario del campo "relationUserProject" del objeto relacionado

    class Meta:
        model = Project
        fields = ['id', 'idrandom', 'name', 'location', 'description', 'relationUserProject']
        # Define los campos que se serializarán/deserializarán y se incluirán en la representación del objeto
        read_only_fields = ['id']
        # Define los campos que serán de solo lectura en la deserialización (es decir, no se permitirá actualizarlos mediante la API)

    def create(self, validated_data):
        # Obtenemos el usuario autenticado de la solicitud
        user = self.context["request"].user
        # Establecemos el valor de relationUserProject en el usuario autenticado
        validated_data["relationUserProject"] = user
        # Creamos el objeto Project usando los datos validados actualizados
        project = Project.objects.create(**validated_data)
        return project

class DevicesSerializer(serializers.ModelSerializer):
    relationUserDevice = serializers.ReadOnlyField(source='relationUserDevice.username')
    # Define un campo de solo lectura "relationUserDevice" que obtiene el nombre de usuario del campo "relationUserDevice" del objeto relacionado

    class Meta:
        model = Devices
        # Asocia el serializador al modelo "Devices"
        fields = [
            "id",  # Campo de identificación del dispositivo
            "name",  # Campo de nombre del dispositivo
            "location",  # Campo de ubicación del dispositivo
            "relationUserDevice",  # Campo de relación con el usuario propietario del dispositivo
        ]
        read_only_fields = ['id']
        # Define los campos que serán de solo lectura en la deserialización (es decir, no se permitirá actualizarlos mediante la API)

    
    def create(self, validated_data):
        # Obtenemos el usuario autenticado de la solicitud
        user = self.context["request"].user
        # Establecemos el valor de relationUserDevice en el usuario autenticado
        validated_data["relationUserDevice"] = user
        # Creamos el objeto relationUserDevice usando los datos validados actualizados
        devices = Devices.objects.create(**validated_data)
        return devices
    
    
class TemplateSerializer(serializers.ModelSerializer):
    relationUserTemplate = serializers.ReadOnlyField(source='relationUserTemplate.username')
    # Define un campo de solo lectura "relationUserTemplate" que obtiene el nombre de usuario del campo "relationUserTemplate" del objeto relacionado

    class Meta:
        model = Template
        # Asocia el serializador al modelo "Template"
        fields = [
            "id",  # Campo de identificación de la plantilla
            "name",  # Campo de nombre de la plantilla
            "sensor",  # Campo de sensor asociado a la plantilla
            "red",  # Campo de red asociada a la plantilla
            "descripcion",  # Campo de descripción de la plantilla
            "relationUserTemplate",  # Campo de relación con el usuario propietario de la plantilla
        ]
        read_only_fields = ['id']
        # Define los campos que serán de solo lectura en la deserialización (es decir, no se permitirá actualizarlos mediante la API)

        
    def create(self, validated_data):
        # Obtenemos el usuario autenticado de la solicitud
        user = self.context["request"].user
        # Establecemos el valor de relationUserDevice en el usuario autenticado
        validated_data["relationUserTemplate"] = user
        # Creamos el objeto relationUserDevice usando los datos validados actualizados
        template = Template.objects.create(**validated_data)
        return template
    
        
class DatosSensoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosSensores
        # Asocia el serializador al modelo "DatosSensores"
        fields = ['name', 'created_at', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12']
        # Define los campos que se serializarán/deserializarán y se incluirán en la representación del objeto
        read_only_fields = ['name', 'created_at', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12']
        # Define los campos que serán de solo lectura en la deserialización (es decir, no se permitirá actualizarlos mediante la API)


class GraphicsSerializer(serializers.ModelSerializer):
    relationUserGraphics = serializers.ReadOnlyField(source='relationUserGraphics.username')
    # Define un campo de solo lectura "relationUserGraphics" que obtiene el nombre de usuario del campo "relationUserGraphics" del objeto relacionado

    class Meta:
        model = graphics
        # Asocia el serializador al modelo "graphics"
        fields = [
            "id",  # Campo de identificación del gráfico
            "titlegraphics",  # Campo de título del gráfico
            "namegraphics",  # Campo de nombre del gráfico
            "aliasgraphics", #Campo de alias del gráfico
            "location",#
            "is_circular",
            "relationUserGraphics",  # Campo de relación con el usuario propietario del gráfico
        ]
        # Define los campos que se serializarán/deserializarán y se incluirán en la representación del objeto
        read_only_fields = ['id']
        # Define los campos que serán de solo lectura en la deserialización (es decir, no se permitirá actualizarlos mediante la API)

    def create(self, validated_data):
        # Obtenemos el usuario autenticado de la solicitud
        user = self.context["request"].user
        # Establecemos el valor de relationUserDevice en el usuario autenticado
        validated_data["relationUserGraphics"] = user
        # Creamos el objeto relationUserDevice usando los datos validados actualizados
        graphicsx = graphics.objects.create(**validated_data)
        return graphicsx
    
