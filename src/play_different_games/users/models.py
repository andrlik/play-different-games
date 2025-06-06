# models.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from play_different_games.users.zones import TIMEZONES

# Create your models here.


class UserProfile(models.Model):
    """
    Custom user profile for PodProducer
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    timezone = models.CharField(
        max_length=100, default=settings.TIMEZONE, choices=TIMEZONES
    )

    def __str__(self) -> str:  # no cov
        return f"{self.user} profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):  # noqa: ARG001
    if created:
        UserProfile.objects.create(user=instance)
