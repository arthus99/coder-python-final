from typing import Any
from django.db.models.query import QuerySet
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
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.cart import Cart
from django.contrib import messages

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from store.models import Category, Product

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import IntegrityError

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


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = "profiles/staff/category-list.html"
    context_object_name = "categories"


@login_required(login_url="url-login")
def CategoryUpdate(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        try:
            category_id = request.POST.get("category_id")
            name = request.POST.get("category_name")
            slug = request.POST.get("category_slug")

            # Obtén la categoría específica
            category = Category.objects.get(id=category_id)
            category.name = name
            category.slug = slug
            category.save()

            messages.success(request, "Categoría Actualizada.")
            response = JsonResponse({"id": category.id, "name": name, "slug": slug})
            return response
        except Category.DoesNotExist:
            return JsonResponse({"error": "Categoría no encontrada"}, status=404)
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "No se ha podido actualizar la categoría"}, status=400
            )
    return JsonResponse(
        {
            "error": "Método "
            + request.method
            + " no permitido."
            + " Accion: "
            + str(request.POST.get("action"))
        },
        status=405,
    )


@login_required(login_url="url-login")
def CategoryAdd(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        try:
            name = request.POST.get("category_name")
            slug = request.POST.get("category_slug")

            # Crear la categoría y almacenarla en una variable
            category = Category.objects.create(name=name, slug=slug)

            messages.success(request, "Categoría creada.")
            response = JsonResponse(
                {"id": category.id, "name": category.name, "slug": category.slug}
            )
            return response
        except IntegrityError:
            return JsonResponse({"error": "La categoría ya existe."}, status=400)
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "No se ha podido insertar la categoría"}, status=400
            )

    return JsonResponse(
        {
            "error": "Método "
            + request.method
            + " no permitido."
            + " Acción: "
            + str(request.POST.get("action"))
        },
        status=405,
    )


class CategoryDelete(LoginRequiredMixin, DeleteView):

    model = Category
    template_name = "profiles/staff/category-delete.html"
    context_object_name = "category"
    success_url = reverse_lazy("CategoryList")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.warning(self.request, "Categoría Borrada.")
        return response


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = "profiles/staff/product-list.html"
    context_object_name = "products"
    queryset = Product.objects.select_related("Category").all()


class ProductAdd(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "profiles/staff/product-add.html"
    fields = "__all__"
    success_url = reverse_lazy("ProductList")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()  # Obtiene todas las categorías
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Producto agregado exitosamente.")
        return response


class ProductDetail(LoginRequiredMixin, DetailView):

    model = Product
    template_name = "profiles/staff/product_detail.html"
    context_object_name = "product"


class ProductUpdate(LoginRequiredMixin, UpdateView):

    model = Product
    template_name = "profiles/staff/product-update.html"
    fields = "__all__"
    success_url = reverse_lazy("ProductList")
    context_object_name = "product"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Producto actualizado.")
        return response


class ProductDelete(LoginRequiredMixin, DeleteView):

    model = Product
    template_name = "profiles/staff/product-delete.html"
    success_url = reverse_lazy("ProductList")
    context_object_name = "product"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Producto eliminado.")
        return response


def contenido_iframe(request):
    return render(request, "profiles/staff/contenido_iframe.html")


def otra_plantilla(request):
    return render(request, "profiles/staff/otra_plantilla.html")
