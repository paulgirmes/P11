"""
Healthier app views
"""

import json

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from sentry_sdk import capture_message
from django.contrib.auth import views as auth_views

from .forms import FoodQuery, Login, Signin
from .models import Food_item


class Reset_Password(auth_views.PasswordResetView):
    """
    Allows for a registered user a to be sent a link via e-mail
    to reset his lost password
    """

    template_name = "healthier/_reset-password.html"
    extra_context = {
        "form1": FoodQuery(auto_id="form1"),
        "user_name": "cher utilisateur",
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.extra_context.update(
                {"user_name": request.user.first_name,}
            )
        return self.render_to_response(self.get_context_data())


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    Diplays a view assessing the reset passwd email was successfully sent
    """

    template_name = "healthier/_password_reset_done.html"
    extra_context = {
        "form1": FoodQuery(auto_id="form1"),
    }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """
    View accessed with the reset mail link to redefine a new password
    """

    template_name = "healthier/_password_reset_confirm.html"
    extra_context = {
        "form1": FoodQuery(auto_id="form1"),
    }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """
    Diplays a view assessing the new passwd was correctly defined
    """

    template_name = "healthier/_password_reset_complete.html"
    extra_context = {
        "form1": FoodQuery(auto_id="form1"),
    }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class PasswordChangeView(auth_views.PasswordChangeView):
    """
    Allows a logged-in user to change his password
    """

    template_name = "healthier/_password_change.html"
    extra_context = {
        "form1": FoodQuery(auto_id="form1"),
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.extra_context.update(
                {"user_name": request.user.first_name,}
            )
        return self.render_to_response(self.get_context_data())


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """
    Diplays a view assessing the passworf was successfully changed
    """

    template_name = "healthier/_password_change_done.html"
    extra_context = {
        "form1": FoodQuery(auto_id="form1"),
    }

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


def home(request):
    request.session.set_expiry(0)
    form = FoodQuery(auto_id="form")
    form1 = FoodQuery(auto_id="form1")
    context = {"form": form, "form1": form1}
    return render(request, "healthier/_index.html", context)


@login_required(login_url="healthier:login")
def myaccount(request):
    form1 = FoodQuery(auto_id="form1")
    context = {
        "form1": form1,
        "user_name": request.user.first_name,
        "user_mail": request.user.email,
    }
    return render(request, "healthier/_user_page.html", context)


@login_required(login_url="healthier:login")
def myfoods(request):
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
        "food_items": "",
    }
    favorites = Food_item.get_favorites(request.user.username)
    message["food_items"] = favorites
    return render(request, "healthier/_my_saved_foods.html", message)


def login(request):
    """
    login and redirects to myaccount or create a new user and redirects
    to myaccount or logout and redirects to home if user logged-in
    """
    request.session["visited"] = True
    form1 = FoodQuery(auto_id="form1")
    if not request.user.is_authenticated:
        sign_form = Signin(auto_id="signin%s")
        log_form = Login(auto_id="login%s")
        message = {
            "form1": form1,
            "sign_form": sign_form,
            "log_form": log_form,
        }
        if request.method == "POST":
            sign_form = Signin(request=request, data=request.POST, auto_id="signin%s")
            try:
                e = sign_form.save()
                if e == True:
                    capture_message("new user added")
                    return redirect(reverse("healthier:myaccount"))
                else:
                    message.update(
                        {"sign_form": sign_form, "modaltoshow": "SigninModal"}
                    )
            except:
                return HttpResponseServerError(
                    "Désolé, une erreur s'est produite dans le traitement de votre inscription !"
                )
        elif "username" in request.GET:
            log_form = Login(request, data=request.GET, auto_id="login%s")
            try:
                log_form.log_user()
                return redirect(reverse("healthier:myaccount"))
            except:
                message.update({"modaltoshow": "LoginModal", "log_form": log_form})

        return render(request, "healthier/_login_signin.html", message)
    else:
        logout(request)
        return redirect(reverse("healthier:home"))
    return render(request, "healthier/_results.html", message)


def contact(request):
    request.session["visited"] = True
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
    }
    return render(request, "healthier/_contact.html", message)


def fooditem(request):
    if "food_id" in request.GET:
        request.session["visited"] = True
        form1 = FoodQuery(auto_id="form1")
        message = {
            "form1": form1,
            "food_item": "",
        }
        message["food_item"] = get_object_or_404(
            Food_item.objects, id=request.GET["food_id"]
        )
        return render(request, "healthier/_food_item.html", message)
    else:
        raise Http404("pas d'aliments recherchés dans la requette")


def general_conditions(request):
    request.session["visited"] = True
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
    }
    return render(request, "healthier/_legal_content.html", message)


def results(request):
    """
    returns results for searched replacement food or error/ 
    allows AJAX to add a replacement item to favorites
    """
    request.session["visited"] = True
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
        "food_items": "",
        "searched": "",
    }
    if "form" in request.GET or "form1" in request.GET:
        # search for replacement food if a form is present in request
        form = FoodQuery(data=request.GET, auto_id="form")
        if form.is_valid():
            results = Food_item.get_searched_food_Item(
                food_name=form.cleaned_data.get("name")
            )
        else:
            message.update({"form": form})
            return render(request, "healthier/_no_results.html", message)
    elif "id" in request.GET:
        # search directly by id if id is present in request
        # (used in the case of the user has had to choose between several items following a foodname search)
        results = Food_item.get_searched_food_Item(food_id=request.GET["id"])
        form = FoodQuery(
            data={"name": results.get("to_be_replaced_item")}, auto_id="form"
        )
    elif request.method == "POST":
        # handle AJAX request to add an item to user's favorites on ly available when logged-in
        results = Food_item.save_favorites(request.POST["value"], request.user)
        return HttpResponse(json.dumps(results))
    else:
        raise Http404("pas d'aliments recherchés dans la requette")

    if results["status"] == "ok":
        message["food_items"] = results["replacement_items"]
        message["searched"] = results["to_be_replaced_item"]
        return render(request, "healthier/_results.html", message)

    elif results["status"] == "choice_to_make":
        if results["to_be_replaced_item"].count() < 100:
            # arbitrary limiting the number of returned choices to 99
            form.add_error(
                None,
                "Il existe "
                + str(results["to_be_replaced_item"].count())
                + " aliments contenant '"
                + form.cleaned_data.get("name")
                + "' !"
                " merci de choisir l'aliment à remplacer dans la liste ci dessous.",
            )
        else:
            # if more than 99 items are found the user is asked to be more specific
            form.add_error(
                None,
                "Il existe "
                + str(results["to_be_replaced_item"].count())
                + " aliments contenant '"
                + form.cleaned_data.get("name")
                + "' !"
                " merci de préciser votre recherche.",
            )
        message.update({"form": form})
        message["searched"] = results["to_be_replaced_item"]

    elif results["status"] == "not_found":
        # if the name searched was not in DB the user is warned
        form.add_error(
            None,
            form.cleaned_data.get("name")
            + " est introuvable dans notre liste d'aliments ! Merci de renouveller votre recherche",
        )
        message.update({"form": form})
        # if no healthier replacement is found in DB the user is also warned
    elif results["status"] == "no_replacement":
        form.add_error(
            None,
            "il n'existe pas à ce jour d'aliment de remplacement plus sain dans notre base de données.",
        )
        message.update({"form": form})
    return render(request, "healthier/_no_results.html", message)


def bad_request_view(request, exception=None):
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
    }
    return render(request, "healthier/_400.html", message, status=400)


def permission_denied_view(request, exception=None):
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
    }
    return render(request, "healthier/_403.html", message, status=403)


def not_found_view(request, exception=None):
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
    }
    return render(request, "healthier/_404.html", message, status=404)


def server_error_view(request, exception=None):
    form1 = FoodQuery(auto_id="form1")
    message = {
        "form1": form1,
    }
    return render(request, "healthier/_500.html", message, status=500)
