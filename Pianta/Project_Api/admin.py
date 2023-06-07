# Actualizado por:
# Yeimmy Katherin Lugo 
# 07/06/2023

from django.contrib import admin

from Project_Api.models import Devices, Project, Template

# Register your models here.

# Importa la clase admin de Django
from django.contrib import admin

# Define una clase ProjectAdmin que personaliza la forma en que se muestra el modelo Project en el panel de administración
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",          # Muestra el campo "name"
        "location",      # Muestra el campo "location"
        "description",   # Muestra el campo "description"
    )

# Define una clase DevicesAdmin que personaliza la forma en que se muestra el modelo Devices en el panel de administración
class DevicesAdmin(admin.ModelAdmin):
    list_display = (
        "id",       # Muestra el campo "id"
        "name",     # Muestra el campo "name"
        "location", # Muestra el campo "location"
    )

# Define una clase TemplateAdmin que personaliza la forma en que se muestra el modelo Template en el panel de administración
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        "id",           # Muestra el campo "id"
        "name",         # Muestra el campo "name"
        "sensor",       # Muestra el campo "sensor"
        "red",          # Muestra el campo "red"
        "descripcion",  # Muestra el campo "descripcion"
    )

# Registra las clases de administrador personalizadas para los modelos correspondientes
admin.site.register(Project, ProjectAdmin)     # Registra el modelo Project con el administrador ProjectAdmin
admin.site.register(Devices, DevicesAdmin)     # Registra el modelo Devices con el administrador DevicesAdmin
admin.site.register(Template, TemplateAdmin)   # Registra el modelo Template con el administrador TemplateAdmin

# Nota: Los modelos Project, Devices y Template deben estar importados y definidos en algún lugar del código antes de registrarlos aquí.
# Esto se puede hacer en otro archivo o en el mismo archivo donde se encuentra este módulo.

