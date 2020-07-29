"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path


from . import views

# debug sentry


def trigger_error(request):
    1 / 0


app_name = "healthier"

urlpatterns = [
    path("", views.home, name="home"),
    path("moncompte/", views.myaccount, name="myaccount"),
    path("mesaliments/", views.myfoods, name="myfoods"),
    path("resultats/", views.results, name="results"),
    path("contact/", views.contact, name="contact"),
    path(
        "mentions_legales/", views.general_conditions,
        name="general_conditions"
    ),
    path("food_item/", views.fooditem, name="fooditem"),
    path("login/", views.login, name="login"),
    path("sentry-debug/", trigger_error),
]
