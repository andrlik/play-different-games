# views.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from rules.contrib.views import PermissionRequiredMixin

from play_different_games.users.forms import UserChangeForm

# Create your views here.


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Where a user can view their details.
    """

    model = User
    slug_url_kwarg = "username"
    slug_field = "username"
    context_object_name = "user"
    template_name = "registration/profile_detail.html"
    permission_required = "users.edit-user"


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Where a user can edit their details.
    """

    model = User
    slug_url_kwarg = "username"
    slug_field = "username"
    context_object_name = "user"
    template_name = "registration/profile_update.html"
    form_class = UserChangeForm
    permission_required = "users.edit-user"
    object: User

    def get_permission_object(self):
        return self.get_object(self.queryset)

    def get_initial(self):
        initial = super().get_initial()
        initial["timezone"] = self.object.profile.timezone  # type: ignore
        return initial

    def form_invalid(self, form):  # no cov
        messages.error(
            self.request, _("Your changes could not be saved. See errors below.")
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.profile.timezone = form.cleaned_data["timezone"]
        user.profile.save()
        user.save()
        messages.success(self.request, _("Your profile has been updated!"))
        return HttpResponseRedirect(
            reverse("users:user-detail", kwargs={"username": user.username})
        )
