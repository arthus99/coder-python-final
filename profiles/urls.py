from django.urls import path
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
]
