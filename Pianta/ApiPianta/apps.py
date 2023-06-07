# Actualizado por:
# Yeimmy Katherin Lugo 
# 07/06/2023

from django.apps import AppConfig

class ApipiantaConfig(AppConfig):
    # Configuración de 'ApiPianta'
    
    # Atributo opcional: especifica el tipo de campo automático a utilizar para las claves principales de los modelos.
    # Si no se especifica, Django utiliza 'AutoField' de forma predeterminada.
    # default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación, debe ser el mismo que se encuentra en la configuración 'INSTALLED_APPS' del archivo settings.py.
    name = 'ApiPianta'

