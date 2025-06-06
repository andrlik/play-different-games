# test_slug_models.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from django.core.exceptions import ImproperlyConfigured

from tests.core.models import (
    InvalidDefaultSluggedModel,
    InvalidSluggedTimeStampedModel,
    SingledSluggedTimeStampedModel,
    ValidSluggedTimetampedModel,
)


def test_invalid_slug_config():
    instance = InvalidSluggedTimeStampedModel(title="Home on the range")
    with pytest.raises(ImproperlyConfigured):
        instance.check_slug_configuration()


def test_invalid_default_slug_config():
    instance = InvalidDefaultSluggedModel(name="Monkey Robinson")
    with pytest.raises(ImproperlyConfigured):
        instance.check_slug_configuration()


def test_valid_slug_config():
    instance = ValidSluggedTimetampedModel(name1="Hello", name2="World")
    assert instance.check_slug_configuration()


def test_valid_single_slug_config():
    instance = SingledSluggedTimeStampedModel(title="John")
    assert instance.check_slug_configuration()
