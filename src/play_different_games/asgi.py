# asgi.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR / "podproducer"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "podproducer.settings")

django_application = get_asgi_application()


async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    else:
        msg = f"Unknown scope type: {scope['type']}"
        raise NotImplementedError(msg)
