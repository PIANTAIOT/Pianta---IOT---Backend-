# Pianta---IOT---Backend-

Resumen

El desarrollo del backend de PIANTA se basa en Django, un framework web escrito en Python. Django se encarga de las operaciones del servidor, incluyendo el almacenamiento, procesamiento y autenticación de datos. Con la ayuda de Django, PIANTA garantiza un backend robusto y escalable que respalda las funcionalidades del front-end de manera eficiente. La combinación de Flutter en el front-end y Django en el backend permite a PIANTA ofrecer una experiencia de usuario fluida, manteniendo la integridad y seguridad de los datos en toda la plataforma.

Abstract
The backend development of PIANTA is based on Django, a web framework written in Python. Django handles server operations, including data storage, processing, and authentication. With the help of Django, PIANTA ensures a robust and scalable backend that supports frontend functionalities efficiently. The combination of Flutter on the frontend and Django on the backend allows PIANTA to offer a seamless user experience while maintaining data integrity and security across the platform.

A continuación, vamos a presentar las API que hemos implementado a lo largo del desarrollo:

1. API de autenticación: Esta API permite a los usuarios registrarse, iniciar sesión y gestionar sus credenciales de acceso. Proporciona endpoints para la creación de cuentas de usuario y la generación de tokens de autenticación.

a. API de Actualización de Usuario:
   - Permite actualizar los detalles de un usuario registrado.
   - Utiliza el modelo de usuario actualmente en uso en el proyecto.
   - Proporciona la capacidad de actualizar información de perfil como nombre, dirección, etc.

b. API de Confirmación de Restablecimiento de Contraseña:
   - Se utiliza para confirmar el restablecimiento de contraseña de un usuario.
   - Permite verificar y procesar la solicitud de restablecimiento de contraseña.
   - Utiliza una vista personalizada para la confirmación de restablecimiento de contraseña.
   - Proporciona una plantilla personalizada para la interfaz de confirmación de restablecimiento de contraseña.

c. API de Inicio de Sesión Personalizada:
   - Permite a los usuarios iniciar sesión en la plataforma.
   - Proporciona una funcionalidad de inicio de sesión personalizada.
   - Registra la fecha y hora del último inicio de sesión exitoso del usuario.

d. API de Registro de Usuarios:
   - Permite registrar nuevos usuarios en la plataforma.
   - Verifica la disponibilidad del correo electrónico y el nombre de usuario proporcionados.
   - Genera un token de autenticación para el usuario registrado.
   - Devuelve los datos del usuario registrado junto con el token de autenticación.

e. API para Envío de Correo Electrónico de Registro:
   - Permite enviar un correo electrónico de verificación durante el proceso de registro.
   - Genera un código de verificación aleatorio.
   - Guarda el código de verificación en la base de datos.
   - Envía el correo electrónico al destinatario con el código de verificación.

f. API de Validación de Token:
   - Permite validar un token durante el proceso de registro.
   - Verifica si el token proporcionado es válido y no ha expirado.
   - Actualiza la fecha de caducidad del token si es válido.
   - Proporciona una respuesta indicando si el token se ha verificado con éxito.

Estas API proporcionan funcionalidades esenciales relacionadas con la gestión de usuarios, autenticación, registro y seguridad en la plataforma.

2. API de sensores: Esta API permite el registro y gestión de sensores IoT. Los endpoints permiten crear, leer, actualizar y eliminar información sobre los sensores, incluyendo su ubicación, tipo de sensor y datos asociados.

La API de sensores proporciona un conjunto de endpoints que permiten interactuar con datos de sensores. Está diseñada para recibir solicitudes y procesar datos relacionados con los sensores.

Cuando se realiza una solicitud POST a la API con datos de sensores en formato JSON, la API procesa esos datos y los guarda en una base de datos. Los datos pueden incluir información como el nombre de la persona asociada con los sensores y los valores de los sensores en sí.

Además de la capacidad de guardar datos de sensores, la API también permite obtener información sobre los datos almacenados. Por ejemplo, se puede realizar una solicitud GET para obtener todos los datos de los sensores almacenados en la base de datos. También es posible obtener información específica de un campo en particular, como el nombre de la persona asociada o la fecha y hora de creación de los datos.

En resumen, la API de sensores proporciona una interfaz para guardar y obtener datos de sensores, lo que permite a los usuarios almacenar y consultar información relacionada con los sensores en una base de datos.


3. API de project:
La API proporciona funcionalidades para manipular y administrar proyectos. A continuación, se describe su funcionalidad general sin mencionar las clases específicas.

La API permite realizar las siguientes operaciones:

a. Listar proyectos: Se puede obtener una lista de todos los proyectos disponibles. Esta lista puede estar filtrada según el usuario que realiza la solicitud. Los proyectos se devuelven en un formato adecuado para la respuesta.

b. Crear un nuevo proyecto: Se puede crear un nuevo proyecto proporcionando los datos necesarios, como un identificador único, nombre, ubicación y descripción. Los datos se validan y, si son válidos, se crea el proyecto y se devuelve como respuesta.

c. Obtener detalles de un proyecto: Se puede obtener información detallada de un proyecto específico proporcionando su identificador único. Si el proyecto existe y pertenece al usuario que realiza la solicitud, se devuelve la información del proyecto.

d. Actualizar un proyecto: Se puede actualizar un proyecto existente proporcionando su identificador único y los datos actualizados, como el nombre, ubicación y descripción. Los datos se validan y, si son válidos, se actualiza el proyecto con los nuevos valores.

e. Eliminar un proyecto: Se puede eliminar un proyecto existente proporcionando su identificador único. Si el proyecto existe y pertenece al usuario que realiza la solicitud, se elimina de la base de datos.

En general, la API requiere autenticación para acceder a estas funcionalidades, lo que significa que los usuarios deben estar autenticados antes de poder listar, crear, obtener, actualizar o eliminar proyectos. Además, la API utiliza un serializador específico para serializar y deserializar los datos de proyecto, lo que garantiza que los datos sean manejados correctamente durante las operaciones de lectura y escritura.

4. Compartir Proyecto:
Estas vistas de la API permiten compartir proyectos existentes y obtener detalles de proyectos compartidos. Para compartir un proyecto, se utiliza un serializador específico y se verifican varios criterios, como la validez del identificador del proyecto y si el proyecto ya ha sido compartido por el usuario actual. Si se cumplen todas las condiciones, se guarda el proyecto compartido en la cuenta del usuario.

Para obtener detalles de un proyecto compartido, se proporciona un identificador único y se realiza una búsqueda en la base de datos. Si se encuentra el proyecto, se devuelve la información detallada del mismo.

En resumen, estas vistas de la API brindan funcionalidades relacionadas con la compartición y recuperación de proyectos compartidos, aplicando validaciones y utilizando serializadores para manipular los datos de manera adecuada.


5. API de devices:

Esta API permite realizar operaciones relacionadas con dispositivos en el contexto de un proyecto.

Permite obtener una lista de dispositivos asociados a un proyecto específico, así como crear nuevos dispositivos para dicho proyecto. También permite obtener, actualizar y eliminar detalles de dispositivos específicos en el contexto de un proyecto.

Para obtener la lista de dispositivos asociados a un proyecto, se realiza una solicitud GET filtrando los dispositivos por el proyecto proporcionado en los argumentos de la URL.

Para crear un nuevo dispositivo, se realiza una solicitud POST con los datos del dispositivo proporcionados en la solicitud, incluyendo el nombre, la ubicación y la relación con el proyecto.

Para obtener los detalles de un dispositivo específico, se realiza una solicitud GET con el identificador del dispositivo y el identificador del proyecto asociado.

Para actualizar los datos de un dispositivo existente, se realiza una solicitud PUT con el identificador del dispositivo y el identificador del proyecto asociado, junto con los nuevos datos del dispositivo.

Para eliminar un dispositivo existente, se realiza una solicitud DELETE con el identificador del dispositivo y el identificador del proyecto asociado.

Estas operaciones aseguran que se realicen dentro del contexto adecuado, es decir, en relación con el proyecto especificado.

6. API de Template:
Esta API permite realizar operaciones relacionadas con plantillas (templates) en el sistema.

Para acceder a esta vista, se requiere que el usuario esté autenticado.

La API permite obtener una lista de todas las plantillas relacionadas con el usuario de la solicitud. También permite crear nuevas plantillas, obtener detalles de una plantilla específica, actualizar los datos de una plantilla existente y eliminar una plantilla.

Para obtener la lista de plantillas relacionadas con el usuario de la solicitud, se realiza una solicitud GET y se filtran las plantillas por el usuario de la solicitud.

Para crear una nueva plantilla, se realiza una solicitud POST con los datos de la plantilla proporcionados en la solicitud, incluyendo el identificador, el nombre, el sensor, la red y la descripción.

Para obtener los detalles de una plantilla específica, se realiza una solicitud GET con el identificador de la plantilla.

Para actualizar los datos de una plantilla existente, se realiza una solicitud PUT con el identificador de la plantilla y se proporcionan los nuevos datos de la plantilla.

Para eliminar una plantilla existente, se realiza una solicitud DELETE con el identificador de la plantilla.

Todas las operaciones se realizan dentro del contexto del usuario autenticado para garantizar la seguridad y la asociación correcta de los datos con el usuario correspondiente.



