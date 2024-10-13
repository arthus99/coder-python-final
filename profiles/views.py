from django.shortcuts import render, redirect
from .forms import CreateUserForm


# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("")

    context = {"form": form}
    return render(request, "profiles/registration/register.html", context=context)


def email_verification_failed(self): ...
def email_verification_sent(self): ...
def email_verification_success(self): ...
def email_verification(self): ...
