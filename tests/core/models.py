# models.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from django.db import models

from play_different_games.core.models import SluggedUUIDTimestampedModel


class ValidSluggedTimetampedModel(SluggedUUIDTimestampedModel):
    """
    A valid model for slug calculation.
    """

    name1 = models.CharField(max_length=50)
    name2 = models.CharField(max_length=50)

    class Meta:
        app_label = "coretestapp"

    class SlugMeta:
        slug_based_on_fields = ["name1", "name2"]


class InvalidSluggedTimeStampedModel(SluggedUUIDTimestampedModel):
    """
    An invalid model configured incorrectly.
    """

    title = models.CharField(max_length=50)

    class Meta:
        app_label = "coretestapp"

    class SlugMeta:
        slug_based_on_fields = ["name"]


class InvalidDefaultSluggedModel(SluggedUUIDTimestampedModel):
    """
    Invalid without SlugMeta set.
    """

    name = models.CharField(max_length=50)

    class Meta:
        app_label = "coretestapp"


class SingledSluggedTimeStampedModel(SluggedUUIDTimestampedModel):
    """
    A valid model with a slug based on a single field.
    """

    title = models.CharField(max_length=50)

    class Meta:
        app_label = "coretestapp"

    class SlugMeta:
        slug_based_on_fields = ["title"]
