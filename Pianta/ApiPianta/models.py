# Actualizado por:
# Yeimmy Katherin Lugo 
# 05/06/2023

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin, Permission
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.contrib.auth.validators import UnicodeUsernameValidator
from datetime import timedelta
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from django.utils import timezone

class UserManager(BaseUserManager):
    # Gestor de usuarios personalizado
    
    def create_user(self, username, email, password=None):
        # Crea y guarda un usuario regular
        
        # Verifica que se proporcione un email válido
        if not email:
            raise ValueError('El usuario debe tener un email válido.')
        
        # Crea una instancia del modelo de usuario con el nombre de usuario y el email normalizado
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        
        # Establece la contraseña proporcionada
        user.set_password(password)
        # Guarda el usuario en la base de datos utilizando la conexión especificada
        user.save(using=self._db)
        # Devuelve el usuario creado
        return user

    def create_superuser(self, username, email, password=None):
        # Crea y guarda un superusuario
        
        # Utiliza el método create_user para crear un usuario regular con los mismos parámetros
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        
        # Establece los atributos de superusuario
        user.is_staff = True
        user.is_superuser = True
        # Guarda el usuario en la base de datos utilizando la conexión especificada
        user.save(using=self._db)
        # Devuelve el usuario creado
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
     # Campo para el nombre de usuario, debe ser único y tener un máximo de 255 caracteres.
    username = models.CharField(unique=True, max_length=255)
    # Campo para el email, debe ser único.
    email = models.EmailField(unique=True)
    # Campo para almacenar la última fecha y hora de inicio de sesión del usuario.
    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)

    #nickname=models.CharField(max_length=55, unique=True)

   # Campo para indicar si el usuario está activo, con un valor predeterminado de True.
    is_active = models.BooleanField(default=True)
    # Campo para indicar si el usuario es personal de staff, con un valor predeterminado de False.
    is_staff = models.BooleanField(default=False)
    
    # Relación ManyToMany con el modelo Group para asignar grupos al usuario.
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='api_users'
    )
    
    # Relación ManyToMany con el modelo Permission para asignar permisos al usuario.
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='api_users'
    )
    
    # Instancia del gestor de usuarios personalizado.
    objects = UserManager()
    # Campo utilizado como nombre de usuario para la autenticación.
    USERNAME_FIELD = 'username'
    # Campos adicionales requeridos para crear un usuario.
    REQUIRED_FIELDS = ['email']
    
    def has_perm(self, perm, obj=None):
        # Método para verificar si el usuario tiene un permiso específico.
        # En este caso, siempre se devuelve True para conceder todos los permisos.
        return True

    def has_module_perms(self, app_label):
        # Método para verificar si el usuario tiene permisos en un módulo específico.
        # En este caso, siempre se devuelve True para conceder permisos en cualquier módulo.
        return True

    def __str__(self) -> str:
        # Método que devuelve una representación en cadena del usuario (en este caso, el ID).
        return str(self.id)
    

class TokensEmail(models.Model):
    token = models.CharField(max_length=6)  # Campo de modelo que almacena un token de longitud máxima de 6 caracteres
    created_at = models.DateTimeField(auto_now_add=True)  # Campo de modelo que registra la fecha y hora de creación del token
    expires_at = models.DateTimeField()  # Campo de modelo que registra la fecha y hora de vencimiento del token
    is_valid = models.BooleanField(default=True)  # Campo de modelo que indica si el token es válido o no (valor predeterminado: True)

    def is_expired(self):
        return self.expires_at <= timezone.now()  # Método que verifica si el token ha expirado comparando su fecha de vencimiento con la hora actual

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)  # Si la fecha de vencimiento no está establecida, se establece 10 minutos en el futuro
        super().save(*args, **kwargs)  # Llama al método `save()` de la clase base para guardar el objeto en la base de datos
        if self.is_valid and self.is_expired():
            self.is_valid = False  # Si el token es válido pero ha expirado, se marca como no válido
            self.save()  # Se vuelve a guardar el objeto para reflejar el cambio en el estado de validez

    @classmethod
    def create_token(cls):
        token_obj = cls.objects.filter(is_valid=True, expires_at__gte=timezone.now()).first()
        # Busca un objeto de token válido cuya fecha de vencimiento sea posterior o igual a la hora actual

        if token_obj:
            token_obj.expires_at = timezone.now() + timedelta(minutes=10)
            token_obj.save()
            # Si se encuentra un token válido, actualiza su fecha de vencimiento para extenderlo otros 10 minutos
        else:
            token = str(uuid4())
            token_obj = cls(token=token)
            token_obj.save()
            # Si no se encuentra un token válido, se crea uno nuevo con un valor UUID (identificador único universal) aleatorio

        return token_obj  # Devuelve el objeto de token creado o actualizado

    @classmethod
    def clean_tokens(cls):
        tokens = cls.objects.filter(is_valid=True)
        # Obtiene todos los objetos de token que aún son válidos

        for token in tokens:
            if token.is_expired():
                token.is_valid = False  # Si el token ha expirado, se marca como no válido
                token.save()  # Se vuelve a guardar el objeto para reflejar el cambio en el estado de validez



#     @classmethod
#     def create_token(cls):
#         from uuid import uuid4
#         token = str(uuid4())
#         token_obj = cls(token=token)
#         token_obj.save()
#         return token_obj

#     @classmethod
#     def clean_tokens(cls):
#         tokens = cls.objects.filter(is_valid=True)
#         for token in tokens:
#             if token.is_expired():
#                 token.is_valid = False
#                 token.save()

# @periodic_task(run_every=crontab(minute='*/10'))
# def clean_tokens():
#     Token.clean_tokens()

#Create your models here.






# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)


    
    
    
    
    
    
    
    
    
    
    
# class User(AbstractBaseUser, PermissionsMixin):
#     # username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         ('username'),
#         max_length=150,
#         unique=True,
#         help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         # validators=[username_validator],
#         error_messages={
#             'unique': ("A user with that username already exists."),
#         },
#     )
#     #first_name = models.CharField(('first name'), max_length=150, blank=True)
#     #last_name = models.CharField(('last name'), max_length=150, blank=True)

#     email = models.EmailField(('email address'), unique=True)
#     is_staff = models.BooleanField(
#         ('staff status'),
#         default=False,
#         help_text=('Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         ('active'),
#         default=True,
#         help_text=(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(('date joined'), default=timezone.now)
#     email = models.EmailField(unique=True)
#     @classmethod
#     def create_user(cls, email):
#         if not email:
#             raise ValueError('The Email field must be set')
#         user = cls(email=email)
#         user.save()
#         return user
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = CustomUserManager()
#     def __str__(self):
#         return self.email
   












    # def generate_otp(self):
    #     import pyotp
    #     totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
    #     return totp.now()
    
    # username_validator = UnicodeUsernameValidator()

    # username = models.CharField(
    #     ('username'),
    #     max_length=150,
    #     unique=True,
    #     help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={
    #         'unique': ("A user with that username already exists."),
    #     },
    #)
    # first_name = models.CharField(('first name'), max_length=150, blank=True)
    # last_name = models.CharField(('last name'), max_length=150, blank=True)
    # email = models.EmailField(('email address'), unique=True)
    # is_staff = models.BooleanField(
    #     ('staff status'),
    #     default=False,
    #     help_text=('Designates whether the user can log into this admin site.'),
    # )
    # is_active = models.BooleanField(
    #     ('active'),
    #     default=True,
    #     help_text=(
    #         'Designates whether this user should be treated as active. '
    #         'Unselect this instead of deleting accounts.'
    #     ),
    # )
    # date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    # objects = UserManager()

    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    # nickname = models.CharField(max_length=55)
    # # profile_picture=ResizedImageField(upload_to,null=True,blank=True)
    
    # def __str__(self):
    #      return self.email

    # def generate_otp(self):
    #     import pyotp
    #     totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')
    #     return totp.now()
    
 
    
# class Project(models.Model):
#     id = models.AutoField(primary_key= True)
#     nombre = models.CharField('Nombre', max_length= 100)
#     descripcion = models.CharField('Descripcion', max_length= 500)

    

#     def __str__(self):
#         return f'{self.nombre} : {self.descripcion}'

# class Device(models.Model):
#     nombre = models.CharField('Nombre', max_length= 100, primary_key= True)

    
#     def __str__(self):
#         return f'{self.nombre}'

# class Template(models.Model):

#     namehardware = models.CharField('Namehardware', max_length=100, primary_key=500)
#     descripcionTemplate = models.CharField('Descripcion', max_length=500)
    
#     def __str__(self):
#         return f'{self.namehardware } : {self.descripcionTemplate}' 