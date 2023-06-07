# Actualizado por:
# Yeimmy Katherin Lugo 
# 07/06/2023

from django.apps import AppConfig


# Define una clase ProjectApiConfig que hereda de AppConfig
class ProjectApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Configura el campo de clave primaria automática como 'BigAutoField'
    name = 'Project_Api'  # Especifica el nombre de la aplicación como 'Project_Api'
