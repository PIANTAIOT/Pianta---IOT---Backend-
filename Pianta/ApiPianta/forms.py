# Actualizado por:
# Yeimmy Katherin Lugo 
# 05/06/2023

from django import forms
# from .models import User

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']


# Formulario personalizado para restablecer contraseña
class CustomPasswordResetForm(forms.Form):
    # Campo para almacenar el 'uid' (identificador de usuario) como un campo oculto en el formulario.
    # Aquí se pueden añadir más campos personalizados según sea necesario para el restablecimiento de contraseña.
    uid = forms.CharField(widget=forms.HiddenInput(), error_messages={'required': 'Uid is required.'})

    # token = forms.CharField(widget=forms.HiddenInput())
    # new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    # new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)

# Constructor de la clase
    def __init__(self, *args, uid=None, **kwargs):
         # Llamada al constructor de la clase padre para inicializar el formulario.
        super().__init__(*args, **kwargs)
         # Configuración inicial del campo 'uid' con el valor proporcionado.
        self.fields['uid'].initial = uid

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password1 = cleaned_data.get("new_password1")
    #     password2 = cleaned_data.get("new_password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return cleaned_data               