# urls.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.urls import path

from play_different_games.users import views

app_name = "users"

urlpatterns = [
    path("<slug:username>/", view=views.UserDetailView.as_view(), name="user-detail"),
    path(
        "<slug:username>/edit/", view=views.UserUpdateView.as_view(), name="user-edit"
    ),
]
