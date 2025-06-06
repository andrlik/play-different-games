# tasks.py
#
# Copyright (c) 2024 - 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Maintenance tasks for playdifferentgames"""

import logging

from django.core.files.storage import default_storage
from prune_media.utils import get_unreferenced_media_paths

logger = logging.getLogger("playdifferentgames")


def remove_unreferenced_media_files() -> tuple[int, int]:
    """Delete unreferenced media files. You can then configure this as a scheduled task.

    Returns:
        Number of deleted media files and the number of failures.
    """
    orphan_files = get_unreferenced_media_paths()
    total_deleted = 0
    total_failed = 0
    for file in orphan_files:
        try:
            default_storage.delete(file)
            total_deleted += 1
        except Exception as err:
            msg = f"Failed to delete {file}. Details: {err}"
            logger.error(msg)
            total_failed += 1
    logger.debug(
        f"Deleted {total_deleted} unreferenced media files, and failed to "
        f"delete {total_failed} unreferenced media files."
    )
    return total_deleted, total_failed
