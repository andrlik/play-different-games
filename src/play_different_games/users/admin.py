# admin.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from play_different_games.users.models import UserProfile

# Register your models here.


class UserProfileInlineAdmin(admin.StackedInline):
    """ModelAdmin for UserProfile"""

    model = UserProfile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInlineAdmin,)
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "profile__timezone",
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
