from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm, CustomSetPasswordForm

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from django.contrib import messages

# from django.contrib.auth import views as auth_views


# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Configuración del correo
            current_site = get_current_site(request)
            subject = "Verificación de su cuenta"
            message = render_to_string(
                "profiles/registration/email-verification.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": user_tokenizer_generate.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)

            return redirect("email-verification-sent")

    context = {"form": form}
    return render(request, "profiles/registration/register.html", context=context)


def email_verification_failed(request):
    return render(request, "profiles/registration/email-verification-failed.html")


def email_verification_sent(request):
    return render(request, "profiles/registration/email-verification-sent.html")


def email_verification_success(request):
    return render(request, "profiles/registration/email-verification-success.html")


def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    # caso Exito
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("email-verification-success")

    # falla
    else:
        return redirect("email-verification-failed")


def url_login(request):
    cart = Cart(request)
    form = LoginForm(request.POST or None)

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                cart.get_cart_from_db(user)
                return redirect("dashboard")
            else:
                form.add_error(None, "Usuario o Contraseña Invalida.")

    context = {"form": form}

    return render(request, "profiles/my-login.html", context)


@login_required(login_url="url-login")
def dashboard(request):
    return render(request, "profiles/dashboard.html")


def url_logout(request):
    cart = Cart(request)
    cart.save_cart_to_db(request.user)
    auth.logout(request)
    messages.success(request, "Sesión Finalizada")
    return redirect("store")


@login_required(login_url="url-login")
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.info(request, "Cuenta Actualizada")
            return redirect("dashboard")

    return render(request, "profiles/profile-management.html", {"user_form": user_form})


@login_required(login_url="url-login")
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        user.delete()
        messages.ERROR(request, "Ha eliminado su Cuenta")
        return redirect("store")

    return render(request, "profiles/delete-account.html")


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "profiles/password/password-reset-form.html"
