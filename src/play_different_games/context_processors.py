# context_processors.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Additional context processors for the project."""

from django.http import HttpRequest

from play_different_games import __version__


def provide_version(request: HttpRequest) -> dict[str, str]:  # noqa: ARG001
    """Provide the project version number to the request context."""

    return {"version": __version__}
