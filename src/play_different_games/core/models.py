# models.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Abstract and base models for the whole project."""

from uuid import uuid4

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from play_different_games.core.utils import generate_unique_slug_for_model


class TimeStampedModel(models.Model):
    """
    An abstract model that adds creation and modified timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    A model that uses a UUID as its primary key.

    Attributes:
        id (uuid): The primary key of the model.
    """

    id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class UniqueSlugModel(models.Model):
    """A model that allows you to define a slug based on other fields.

    Attributes:
        slug (str): A unique slug for this instance.
    """

    slug = models.SlugField(
        allow_unicode=True,
        max_length=150,
        blank=True,
        null=False,
        unique=True,
        help_text=_("Slug for this record."),
    )

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """
        Adds a new key to the Meta class enabling us to use `slug_based_on_fields`
        with a default of `['title',]`.
        In actual subclassed models you can override with:
            class SlugMeta:
                slug_based_on_fields = ['field1', 'field2', ...]
        """
        cls = self.__class__
        my_meta = getattr(cls, "SlugMeta", None)
        cls._slug_meta = my_meta  # type: ignore
        super().__init__(*args, **kwargs)

    class SlugMeta:
        slug_based_on_fields = ["title"]

    def save(self, *args, **kwargs):
        """
        Save method from Django, but we also generate a unique slug if not already
        defined.
        """
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    def check_slug_configuration(self) -> None:
        """
        Does a sanity check to ensure the slug configuration and save operations.
        Raise `ImproperlyConfigured` if fails test.
        """
        for x in self._slug_meta.slug_based_on_fields:  # type: ignore
            if not hasattr(self, x):
                msg = f"Cannot find field '{x}' in model to generate slug from."
                raise ImproperlyConfigured(msg)

    def generate_slug(self) -> str:
        """
        Gathers the slug source field data and sets the slug based on the result of
        a unique slug.
        """
        self.check_slug_configuration()
        slug_src: str = ""
        src_fields = self._slug_meta.slug_based_on_fields  # type: ignore
        if len(src_fields) > 1:
            for x in src_fields:
                slug_src = f"{slug_src} {getattr(self, x)}"
        else:
            slug_src = getattr(self, src_fields[0])
        return generate_unique_slug_for_model(
            type(self), text=slug_src, allow_unicode=True
        )


class SluggedUUIDTimestampedModel(UUIDModel, TimeStampedModel, UniqueSlugModel):
    """
    Combines the timestamped, UUID, and Unique Slug models.

    Attributes:
        id (uuid): The primary key of the model.
        slug (str): A unique slug for this instance.
        created_at (datetime): The date and time when the record was created.
        modified_at (datetime): The date and time when the record was last updated.
    """

    class Meta:
        abstract = True

    class SlugMeta:
        # Placeholder value, you should override this on your models.
        slug_based_on_fields = ["title"]
