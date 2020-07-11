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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from healthier import views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", include("healthier.urls", namespace="healthier")),
    path('accounts/password_reset/',
        views.Reset_Password.as_view(),
        name='password_reset',
    ),
    path('accounts/reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('accounts/password_reset/done/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path('account/password_reset_complete/',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('account/password_change/',
        views.PasswordChangeView.as_view(),
        name='password_change',
    ),
    path('account/password_change/done/',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
]

handler404 = 'healthier.views.not_found_view'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns