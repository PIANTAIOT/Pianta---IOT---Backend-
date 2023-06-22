
# 07/06/2023

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ApiPianta.models import User
import pytz
from datetime import datetime
from datetime import timedelta


# Create your models here.

# Define la clase Project que hereda de models.Model
class Project(models.Model):
    id = models.AutoField(primary_key=True)  # Define un campo AutoField llamado 'id' como clave primaria
    idrandom = models.UUIDField(default=uuid.uuid4, editable=False)  # Genera un campo UUID único llamado 'idrandom' con un valor predeterminado generado automáticamente
    name = models.CharField(max_length=300, blank=False, null=False)  # Define un campo CharField llamado 'name' con una longitud máxima de 300 caracteres y no permite valores en blanco ni nulos
    location = models.CharField(max_length=1000, blank=False, null=False)  # Define un campo CharField llamado 'location' con una longitud máxima de 1000 caracteres y no permite valores en blanco ni nulos
    description = models.CharField(max_length=300, blank=False, null=False)  # Define un campo CharField llamado 'description' con una longitud máxima de 300 caracteres y no permite valores en blanco ni nulos
    relationUserProject = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', default=None)  # Define una relación ForeignKey con el modelo User, establece el comportamiento de eliminación en cascada y establece el atributo relacionado como 'projects'

# Define la clase SharedProject que hereda de models.Model
class SharedProject(models.Model):
    id = models.AutoField(primary_key=True)  # Define un campo AutoField llamado 'id' como clave primaria
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Define una relación ForeignKey con el modelo User y establece el comportamiento de eliminación en cascada
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Define una relación ForeignKey con el modelo Project y establece el comportamiento de eliminación en cascada
    timestamp = models.DateTimeField(auto_now_add=True)  # Define un campo DateTimeField llamado 'timestamp' que se establece automáticamente en la fecha y hora actual cuando se crea un objeto





# Define la clase Devices que hereda de models.Model
class Devices(models.Model):
    id = models.AutoField(primary_key=True)  # Define un campo AutoField llamado 'id' como clave primaria
    name = models.CharField(max_length=30, blank=False, null=False)  # Define un campo CharField llamado 'name' con una longitud máxima de 30 caracteres y no permite valores en blanco ni nulos
    location = models.CharField(max_length=1000, blank=False, null=False)  # Define un campo CharField llamado 'location' con una longitud máxima de 100 caracteres y no permite valores en blanco ni nulos
    template = models.CharField(max_length=1000, blank=False, default=False)
    relationProject = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='devices', default=None)
    
# Define la clase Template que hereda de models.Model
class Template(models.Model):
    id = models.AutoField(primary_key=True)  # Define un campo AutoField llamado 'id' como clave primaria
    name = models.CharField(max_length=30, blank=False, null=False)  # Define un campo CharField llamado 'name' con una longitud máxima de 30 caracteres y no permite valores en blanco ni nulos
    sensor = models.CharField(max_length=50, blank=False, null=False)  # Define un campo CharField llamado 'sensor' con una longitud máxima de 50 caracteres y no permite valores en blanco ni nulos
    red = models.CharField(max_length=50, blank=False, null=False)  # Define un campo CharField llamado 'red' con una longitud máxima de 50 caracteres y no permite valores en blanco ni nulos
    descripcion = models.CharField(max_length=100, blank=False, null=False)  # Define un campo CharField llamado 'descripcion' con una longitud máxima de 100 caracteres y no permite valores en blanco ni nulos
    relationUserTemplate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates', default=None)  # Define una relación ForeignKey con el modelo User, establece el comportamiento de eliminación en cascada y establece el atributo relacionado como 'templates'



# Define la clase DatosSensores que hereda de models.Model
class DatosSensores(models.Model):
    name = models.CharField(max_length=255)  # Define un campo CharField llamado 'name' con una longitud máxima de 255 caracteres
    v1 = models.FloatField()  # Define un campo FloatField llamado 'v1'
    v2 = models.FloatField()  # Define un campo FloatField llamado 'v2'
    v3 = models.FloatField()  # Define un campo FloatField llamado 'v3'
    v4 = models.FloatField()  # Define un campo FloatField llamado 'v4'
    v5 = models.FloatField()  # Define un campo FloatField llamado 'v5'
    v6 = models.FloatField()  # Define un campo FloatField llamado 'v6'
    v7 = models.FloatField()  # Define un campo FloatField llamado 'v7'
    v8 = models.FloatField()  # Define un campo FloatField llamado 'v8'
    v9 = models.FloatField()  # Define un campo FloatField llamado 'v9'
    v10 = models.FloatField()  # Define un campo FloatField llamado 'v10'
    v11 = models.FloatField()  # Define un campo FloatField llamado 'v11'
    v12 = models.FloatField()  # Define un campo FloatField llamado 'v12'
    created_at = models.DateTimeField()  # Define un campo DateTimeField llamado 'created_at'
    relationTemplatePin = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='pin', default=None)  # Define una relación ForeignKey con el modelo User, establece el comportamiento de eliminación en cascada y establece el atributo relacionado como 'pin'



    def _str_(self):
        return f"{self.name} - {self.valor}"
    def save(self, *args, **kwargs):
        # Establecer la zona horaria correspondiente a Colombia
        timezone = pytz.timezone('America/Bogota')
        # Obtener la fecha y hora actual con la zona horaria del servidor
        now = datetime.now()
        # Convertir la fecha y hora actual a la zona horaria de Colombia
        colombia_time = timezone.localize(now)
        # Ajustar la hora para tener en cuenta la diferencia horaria con UTC
        adjusted_time = colombia_time - timedelta(hours=5)
        # Establecer el campo created_at con la hora ajustada
        self.created_at = adjusted_time
        super().save(*args, **kwargs)
# Create your models here.

# Define la clase graphics que hereda de models.Model
class graphics(models.Model):
    id = models.AutoField(primary_key=True)  # Define un campo AutoField llamado 'id' como clave primaria
    titlegraphics = models.CharField(max_length=1000, blank=True, null=False)  # Define un campo CharField llamado 'titlegraphics' con una longitud máxima de 1000 caracteres y permite valores en blanco
    namegraphics = models.CharField(max_length=1000, blank=True, null=False)  # Define un campo CharField llamado 'namegraphics' con una longitud máxima de 1000 caracteres y permite valores en blanco
    aliasgraphics = models.CharField(max_length=1000, blank=True, null=False)  # Define un campo CharField llamado 'aliasgraphics' con una longitud máxima de 1000 caracteres y permite valores en blanco
    location = models.CharField(max_length=1000, blank=False, default=False)  # Define un campo CharField llamado 'location' con una longitud máxima de 100 caracteres y no permite valores en blanco ni nulos
    color = models.CharField(max_length=1000, blank=False, default=False)
    is_circular = models.BooleanField(default=False)
    relationTemplateGraphics = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='graphics', default=None)  # Define una relación ForeignKey con el modelo User, establece el comportamiento de eliminación en cascada y establece el atributo relacionado como 'graphics'


    