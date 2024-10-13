from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


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
