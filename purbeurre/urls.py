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
    path('reset_mdp/',
        views.Reset_Password.as_view(),
        name='password_reset',
    ),
    path('reset_mdp/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('reset_mdp/ok/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path('reset_mdp_effectue/',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('changement_mdp/',
        views.PasswordChangeView.as_view(),
        name='password_change',
    ),
    path('changement_mdp/ok/',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
]

handler400 = 'healthier.views.bad_request_view'
handler403 = 'healthier.views.permission_denied_view'
handler404 = 'healthier.views.not_found_view'
handler500 = 'healthier.views.server_error_view'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns