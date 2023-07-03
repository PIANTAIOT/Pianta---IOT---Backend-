from django.urls import path
from Project_Api import views
from .views import DevicesListApiView, ProjectDetailApiView, ProjectListApiView, DevicesDetailApiView, TemplateDetailApiView, TemplateListApiView, SharedProjectView, ShareProjectView,  obtener_datos_sensores, datos_sensores, DeleteSharedProjectView, SharedProjectList, GraphicsApiView, GraphicsApiDetailView, save_DatosSensores, TemplateGetShared#, SharedrandonView

urlpatterns = [
    path('project/', ProjectListApiView.as_view(), name="Project_List"),
    path('project/<int:project_id>/devices/', DevicesListApiView.as_view(), name='devices-list'),
    path('template/', TemplateListApiView.as_view(), name="template_List"),
    path('template/shared/', TemplateGetShared.as_view(), name="template_shared"),
    path('graphics/<int:id>/', GraphicsApiView.as_view(), name="graphics_list"),
    path('graphics/<int:id>/<int:graphics_id>/', GraphicsApiDetailView.as_view(), name="graphics_detail"),
    path('project/<int:project_id>/', ProjectDetailApiView.as_view(), name="Project_detail"),
    path('project/share/', ShareProjectView.as_view(), name='share_project'),
    path('project/detail/share/<uuid:idrandom>/', SharedProjectView.as_view(), name='project_detail_share'),
    path('project/share/<int:pk>/', DeleteSharedProjectView.as_view(), name='delete-shared-project'),
    path('relationshared/projects/', SharedProjectList.as_view(), name='shared/projects/list'),
    path('devices/<int:device_id>/<int:project_id>/', DevicesDetailApiView.as_view(), name="Device_detail"),
    path('template/<int:template_id>/', TemplateDetailApiView.as_view(), name="Template_detail"),
    path('api/DatosSensores/<int:id>/',save_DatosSensores.as_view(), name='save_DatosSensores'),
    path('datos-sensores/', obtener_datos_sensores, name='obtener_datos_sensores'),
    path('datos-sensores/<str:field>/<int:id>/', datos_sensores.as_view(), name='obtener_datos_sensores'),
]   