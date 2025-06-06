# utils.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.utils.text import slugify

logger = logging.getLogger("play_different_games")


def generate_unique_slug_for_model(
    model_class: type[Model],
    text: str,
    slug_field: str | None = "slug",
    max_length_override: int | None = None,
    allow_unicode: bool | None = None,
) -> str:
    """
    Given a text and model class, generate a unique slug based on that text.

    Args:
        model_class (Model): A class based upon `django.db.models.Model`.
        text (str): The text to convert to a slug.
        slug_field (str): The name of the field for saving the slug. Default 'slug'.
        max_length_override (int | None): Max length in characters for resulting slug.
        allow_unicode (bool | None): Allow Unicode characters in slug. Default None.
    Returns:
        The generated slug as a str.
    """
    if allow_unicode is None:
        allow_unicode = False
    unique_found: bool = False
    has_next: bool = False
    next_val: int = 1
    max_length: int
    if not max_length_override:
        logger.debug("Setting max_length of slug from field definition.")
        max_length: int = model_class._meta.get_field(slug_field).max_length  # type: ignore
    else:
        logger.debug(
            f"User override value for max length of slug with [{max_length_override}]"
        )
        max_length = max_length_override
    base_slug = slugify(text[:max_length], allow_unicode=allow_unicode)
    logger.debug(f"Base slug is set to '{base_slug}'.")
    slug = base_slug
    while not unique_found:
        logger.debug(f"Testing uniqueness of slug '{slug}'...")
        try:
            model_class.objects.get(**{str(slug_field): slug})
        except ObjectDoesNotExist:
            logger.debug("Slug is unique!")
            unique_found = True
        if not unique_found:
            logger.debug("Slug is not unique yet.")
            if has_next:
                slug = base_slug
            if len(slug) >= max_length:
                slug = slug[: max_length - (len(str(next_val)) + 1)]
            slug = slug + f"-{next_val}"
            has_next = True
            next_val += 1
    return slug
