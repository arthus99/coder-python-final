from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User
from django import forms

from django.utils.translation import gettext_lazy as _

from django.forms.widgets import PasswordInput, TextInput


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        # Especificación de los campos a incluir en el formulario
        fields = [
            "username",
            "password",
        ]
        # Personalización de las etiquetas de los campos
        labels = {"username": "Usuario", "password": "Contraseña"}


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar Contraseña",
        }
        help_texts = {
            "username": "Requerido. 150 carácteres o menos. Sólo letras numeros y @/./+/-/_ ",
            "password1": "",
            "password2": "",
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].help_text = None
        self.fields["password2"].label = "Confirmar Contraseña"
        self.fields["password2"].help_text = (
            "Ingrese la misma contraseña para verificar"
        )
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo ya existe, por favor intente denuevo."
            )
        if len(email) >= 350:
            raise forms.validationError("Error: Su correo es muy largo.")

        return email


class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        # Llamada correcta al constructor de la clase base
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["username"].label = "usuario"
        self.fields["username"].help_text = (
            "Requerido. 150 carácteres o menos. Sólo letras numeros y @/./+/-/_ ",
        )
        self.fields["email"].label = "Correo electrónico"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                "Este correo ya existe, por favor intente denuevo."
            )
        if len(email) >= 350:
            raise forms.validationError("Error: Su correo es muy largo.")

        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        help_text=_("Introduce una nueva contraseña segura."),
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label=_("Confirmar nueva contraseña"),
        help_text=_("Repite la nueva contraseña para confirmarla."),
        widget=forms.PasswordInput,
    )
