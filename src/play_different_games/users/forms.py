# forms.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from play_different_games.users.zones import TIMEZONES


class UserChangeForm(forms.ModelForm):
    timezone = forms.ChoiceField(choices=TIMEZONES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = _("Given name")
        self.fields["last_name"].label = _("Surname")

    class Meta:
        model = User
        fields = ["first_name", "last_name"]
