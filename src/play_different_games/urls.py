# urls.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, messages
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect
from django.urls import include, path, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import defaults as default_views
from django.views.generic import TemplateView

# from play_different_games import views

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls


def confirm_password_change(request):  # no cov
    messages.success(request, _("Password changed successfully!"))
    return HttpResponseRedirect(
        reverse_lazy("users:user-detail", kwargs={"username": request.user.username})
    )


urlpatterns = [
    path("", view=TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "400/",
        default_views.bad_request,
        kwargs={"exception": Exception("Bad Request!")},
    ),
    path(
        "403/",
        default_views.permission_denied,
        kwargs={"exception": Exception("Permission Denied!")},
    ),
    path(
        "404/",
        default_views.page_not_found,
        kwargs={"exception": Exception("Not Found!")},
    ),
    path(
        "500/",
        default_views.server_error,
        kwargs={"exception": Exception("Server Error!")},
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path("accounts/password_change/done/", confirm_password_change),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/", include("play_different_games.users.urls", namespace="users")),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG and not settings.TESTING:  # no cov
    urlpatterns += debug_toolbar_urls()  # type: ignore
