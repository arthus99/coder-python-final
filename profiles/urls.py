from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "email_verification_failed/",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
    path(
        "email_verification_sent/",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email_verification_success/",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path(
        "email_verification/<str:uidb64>/<str:token>/",
        views.email_verification,
        name="email-verification",
    ),
    path("login/", views.url_login, name="url-login"),
    path("logout/", views.url_logout, name="url-logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile-management/", views.profile_management, name="profile-management"),
    path("delete-account/", views.delete_account, name="delete-account"),
    # Adminostración del reinicio de passwords con CBV
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="profiles/password/password-reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="profiles/password/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.MyPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="profiles/password/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("category_list/", views.CategoryList.as_view(), name="CategoryList"),
    path("category_update/", views.CategoryUpdate, name="CategoryUpdate"),
    path("category_delete/<pk>", views.CategoryDelete.as_view(), name="CategoryDelete"),
    path("category_add/", views.CategoryAdd, name="CategoryAdd"),
    path("product_list/", views.ProductList.as_view(), name="ProductList"),
    path("product_detail/<pk>", views.ProductDetail.as_view(), name="ProductDetail"),
    path("product_update/<pk>", views.ProductUpdate.as_view(), name="ProductUpdate"),
    path("product_delete/<pk>", views.ProductDelete.as_view(), name="ProductDelete"),
    path("product_add/", views.ProductAdd.as_view(), name="ProductAdd"),
    path("contenido_iframe/", views.contenido_iframe, name="contenido_iframe"),
    path("otra_plantilla/", views.otra_plantilla, name="otra_plantilla"),
]
