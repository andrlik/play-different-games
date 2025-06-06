# conftest.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Fixtures and setup for test suite."""

import subprocess

import pytest
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
    pre_delete,
    pre_save,
)

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture(autouse=True)
def use_test_media(request, settings):
    settings.MEDIA_ROOT = str(settings.PROJECT_DIR / "testmedia")

    def remove_test_media():
        subprocess.run(["rm", "-rf", settings.MEDIA_ROOT], check=False)  # noqa: S603 S607

    request.addfinalizer(remove_test_media)


@pytest.fixture
def mute_signals(request):
    if "enable_signals" in request.keywords:
        return

    signals = [pre_save, post_save, pre_delete, post_delete, m2m_changed]
    restore = {}
    for signal in signals:
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        for signal, receivers in restore.items():
            signal.receivers = receivers

    request.addfinalizer(restore_signals)


@pytest.fixture
def user(tp):
    user = tp.make_user("u1")
    yield user
    user.delete()


@pytest.fixture(autouse=True)
def use_md5_hashing(settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
