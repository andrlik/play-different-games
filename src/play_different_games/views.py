# views.py
#
# Copyright (c) 2025 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Views used to override views to add htmx"""

from typing import TYPE_CHECKING, ClassVar

from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest:
    htmx: HtmxDetails | None


class HtmxPartialMixin:
    """
    Modifies the template to the specified partial if the request is htmx.
    """

    partial_label: ClassVar[str | None] = None
    if TYPE_CHECKING:
        request: HtmxHttpRequest
        template_name: str | None = None

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            if self.template_name is not None and self.partial_label is not None:
                self.template_name += f"#{self.partial_label}"
        return super().get_template_names()  # type: ignore
