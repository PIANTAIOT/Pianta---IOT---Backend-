# Actualizado por:
# Yeimmy Katherin Lugo 
# 05/06/2023

from rest_framework import serializers
from dj_rest_auth.serializers  import LoginSerializer
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import gettext as _
from django.conf import settings
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from dj_rest_auth.serializers import LoginSerializer, TokenSerializer, PasswordResetSerializer, UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.core.mail import EmailMessage


UserModel = get_user_model()  # Obtiene la clase del modelo de usuario configurado en Django
from dj_rest_auth.serializers import UserDetailsSerializer  # Importa el serializador UserDetailsSerializer de dj_rest_auth

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel  # Especifica el modelo que se utilizará para el serializador (modelo de usuario personalizado)
        fields = ('username', 'email')  # Especifica los campos que se incluirán en el serializador para la actualización (nombre de usuario y correo electrónico)

# class CustomUserDetailsSerializer(UserDetailsSerializer):
#     last_login = serializers.DateTimeField(read_only=True)
#     class Meta(UserDetailsSerializer.Meta):
#         fields = UserDetailsSerializer.Meta.fields + ('last_login',)

class NewRegisterSerializer(serializers.Serializer):
    # Campo de serializador que representa el nombre de usuario del usuario a registrar
    # La longitud máxima del campo se obtiene del modelo de usuario configurado en Django
    username = serializers.CharField(max_length=UserModel._meta.get_field('username').max_length, required=False)
    
    # Campo de serializador que representa la dirección de correo electrónico del usuario a registrar
    email = serializers.EmailField(required=False)

    # Campo de serializador que representa la contraseña del usuario a registrar
    # `write_only=False` indica que el campo también se puede leer, no solo escribir
    # `required=False` indica que el campo no es obligatorio y se puede omitir en la solicitud
    password = serializers.CharField(write_only=False, required=False)

    def create(self, validated_data):
        with transaction.atomic():  # Inicia una transacción de base de datos para asegurar la atomicidad de la creación de usuario y token
            user = UserModel.objects.create_user(
                username=validated_data['username'],  # Crea un nuevo usuario con el nombre de usuario proporcionado
                email=validated_data['email'],  # Establece el correo electrónico del usuario
                password=validated_data['password'],  # Establece la contraseña del usuario
            )
            Token.objects.create(user=user)  # Crea un token de autenticación para el usuario recién creado
        return user  # Devuelve el objeto de usuario recién creado

# class CustomPasswordResetSerializer(PasswordResetSerializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         # Check if the email is registered in the database
#         try:
#             user = UserModel.objects.get(email=value)
#         except UserModel.DoesNotExist:
#             raise serializers.ValidationError(_('This email is not registered.'))
#         return value

    # def send_reset_email(self, user):
    #     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    #     token = PasswordResetTokenGenerator().make_token(user)
    #     reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
    #     reset_url = 'http://127.0.0.1:8000/' + reset_link  # Reemplaza 'your_website.com' por tu dominio
    #     message = 'Please use this link to reset your password:\n\n' + reset_url
    #     email = EmailMessage(
    #         subject='Password reset',
    #         body=message,
    #         from_email=settings.EMAIL_HOST_USER,
    #         to=[user.email],
    #     )
    #     email.send()

    # def save(self, **kwargs):
    #     # Use Django's built-in password reset mechanisms to send a reset email to the user
    #     email = self.validated_data['email']
    #     for user in UserModel.objects.filter(email=email):
    #         self.send_reset_email(user)
    #         # send_mail(
    #         #     _('Password reset'),
    #         #     _('Please click on the following link to reset your password'),
    #         #     from_email=settings.DEFAULT_FROM_EMAIL,
    #         #     recipient_list=[user.email],
    #         #     fail_silently=False,
    #         # )

# La clase `NewLoginSerializer` hereda de `LoginSerializer` sin agregar ninguna funcionalidad adicional.                            
class NewLoginSerializer(LoginSerializer):
    pass
# La clase `NewTokenSerializer` hereda de `TokenSerializer` sin agregar ninguna funcionalidad adicional.
class NewTokenSerializer(TokenSerializer):
    pass

# La clase `ForgotPasswordSerializer` hereda de `serializers.Serializer` y define un campo llamado `email` de tipo `serializers.EmailField()`.
# Este serializer se utiliza para solicitar la recuperación de contraseña mediante el envío de un correo electrónico.
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

# La clase `ResetPassowrdSerializer` hereda de `serializers.Serializer` y define dos campos: `password` y `confirm_password`, ambos de tipo `serializers.CharField()`.
# Este serializer se utiliza para realizar el restablecimiento de contraseña, donde el usuario proporciona una nueva contraseña y la confirma.   
class ResetPassowrdSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True, style={'input_type': 'password'})
    # Define un campo llamado `new_password1` de tipo `serializers.CharField()` que se utiliza para capturar la nueva contraseña del usuario.
    # El parámetro `required=True` indica que este campo es obligatorio.
    # El parámetro `style={'input_type': 'password'}` se utiliza para indicar que el campo debe mostrarse como un campo de contraseña en el formulario.

    new_password2 = serializers.CharField(required=True, style={'input_type': 'password'})
    # Define un campo llamado `new_password2` de tipo `serializers.CharField()` que se utiliza para capturar la confirmación de la nueva contraseña del usuario.
    # El parámetro `required=True` indica que este campo es obligatorio.
    # El parámetro `style={'input_type': 'password'}` se utiliza para indicar que el campo debe mostrarse como un campo de contraseña en el formulario.

    uid = serializers.CharField(required=True)
    # Define un campo llamado `uid` de tipo `serializers.CharField()` que se utiliza para capturar el identificador único del usuario.
    # El parámetro `required=True` indica que este campo es obligatorio.

    token = serializers.CharField(required=True)
    # Define un campo llamado `token` de tipo `serializers.CharField()` que se utiliza para capturar el token de restablecimiento de contraseña.
    # El parámetro `required=True` indica que este campo es obligatorio.
    
    def __str__(self):
        return f"CustomPasswordResetConfirmSerializer(uid={self.validated_data.get('uid')})"
    # Método __str__() que devuelve una representación en forma de cadena del objeto `CustomPasswordResetConfirmSerializer`.
    # Utiliza el método `validated_data.get('uid')` para obtener el valor del campo `uid` del objeto validado.

    def create(self, validated_data):
        # Obtiene el uid y el token del serializer
        uid = validated_data.get('uid')
        token = validated_data.get('token')
        # Método `create()` que se utiliza para crear una instancia del objeto `CustomPasswordResetConfirmSerializer`.
        # Recibe `validated_data` como argumento, que es un diccionario que contiene los datos validados del serializer.
        # Utiliza el método `validated_data.get('uid')` para obtener el valor del campo `uid` del objeto validado y asignarlo a la variable `uid`.
        # Utiliza el método `validated_data.get('token')` para obtener el valor del campo `token` del objeto validado y asignarlo a la variable `token`.


        # Obtiene el usuario correspondiente al uid
        try:
            #uid = force_text(urlsafe_base64_decode(uid))
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
            # Manejo de excepciones que captura varios tipos de excepciones: TypeError, ValueError, OverflowError y UserModel.DoesNotExist.
            # Si se produce alguna de estas excepciones, se establece la variable `user` en None.

        # Verifica que el token sea válido
        if user is not None and default_token_generator.check_token(user, token):
            # Actualiza la contraseña del usuario
            password = validated_data.get('new_password1')
            user.set_password(password)
            user.save()
            return user
            # Se verifica si la variable `user` no es None y si el token es válido utilizando el método `check_token()` del generador de tokens predeterminado (default_token_generator).
            # Si el usuario existe y el token es válido, se obtiene la nueva contraseña del diccionario `validated_data` y se establece como la nueva contraseña del usuario.
            # Luego, se guarda el usuario en la base de datos y se devuelve el usuario.

        raise ValidationError('Invalid reset password token.')
        # Si no se cumple ninguna de las condiciones anteriores, se genera una excepción de validación (ValidationError) indicando que el token de restablecimiento de contraseña no es válido.

        
    # def create(self, validated_data):
    #     user = UserModel.objects.create_user(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         password=validated_data['password']
    #     )

    #     # Generate token for the new user
    #     token = Token.objects.create(user=user)

    #     # Authenticate user and login
    #     auth_user = authenticate(
    #         username=validated_data['username'],
    #         password=validated_data['password']
    #     )
    #     login(self.context['request'], auth_user)

    #     return {'token': token.key}
    
    # def save(self, request):
    #     user = super().save(request)
    #     Token.objects.create(user=user)
    #     return user
  





  # first_name=serializers.CharField()
    # last_name=serializers.CharField()
    #nickname=serializers.CharField()
    # def custom_signup(self, request, user):
        # user.first_name=request.data['first_name']
        # user.last_name=request.data['last_name']
        #user.nickname=request.data['nickname']
      #  user.save()





# class UserSerializer(serializers.ModelSerializer):
    
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'email', 'password']

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         #user = get_user_model().objects.create(email=validated_data['email'], **validated_data)
#         user = get_user_model().objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user



# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Project
#         fields = (
#             'id',
#             'nombre',
#             'descripcion',
#         )

# class DeviceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Device
#         fields = (
#             'nombre',
#         )
        
# class TemplateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Template
#         fields = (
#             'namehardware',
#             'descripcionTemplate',
#         )