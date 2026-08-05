from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import RegisterForm


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully!"
            )

            return redirect("product_list")

    else:

        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form
    })


from django.contrib.auth import authenticate, login

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("product_list")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "accounts/login.html")


def user_logout(request):

    return redirect("product_list")