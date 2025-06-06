# rules.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from typing import Any

import rules
from django.contrib.auth.models import User


@rules.predicate  # type: ignore
def is_self(user: User, obj: Any) -> bool:
    return user == obj


can_edit_profile = is_self | rules.is_superuser  # type: ignore

rules.add_perm("users.edit-user", can_edit_profile)  # type: ignore
