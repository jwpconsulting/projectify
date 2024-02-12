# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Corporate admin."""
from typing import Any, Optional

from django import forms
from django.contrib import (
    admin,
)
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from projectify.corporate.models.coupon import Coupon
from projectify.corporate.services.coupon import coupon_create
from projectify.user.models import User

from . import (
    models,
)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin[models.Customer]):
    """Customer Admin."""

    list_display = ("workspace_title", "seats", "subscription_status")
    list_filter = ("subscription_status",)
    list_select_related = ("workspace",)
    readonly_fields = (
        "uuid",
        "stripe_customer_id",
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Customer) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin[Coupon]):
    """Customer Admin."""

    list_display = ("code", "customer", "used", "seats")
    readonly_fields = ("code",)
    list_select_related = ("customer",)

    class CouponForm(forms.ModelForm):
        """Form for coupon creation."""

        seats = forms.IntegerField(min_value=1, initial=1)
        code_prefix = forms.CharField(min_length=5, max_length=50)

        class Meta:
            """Specify model."""

            fields = ("seats",)
            model = Coupon

    def get_form(
        self,
        request: HttpRequest,
        obj: Optional[Coupon] = None,
        change: bool = False,
        **kwargs: Any,
    ) -> type[forms.ModelForm]:
        """Return a custom form for creation, otherwise return regular."""
        if obj:
            return super().get_form(request, obj, change, **kwargs)  # type: ignore[no-any-return]
        return self.CouponForm

    def save_model(
        self,
        request: HttpRequest,
        obj: Coupon,
        form: forms.Form,
        change: bool = False,
    ) -> None:
        """Override save_form for creation."""
        if change:
            super().save_model(request, obj, form, change)
            return

        user = request.user
        if not isinstance(user, User):
            raise ValueError("Expected user to be User")
        data = form.cleaned_data
        coupon_create(
            who=user,
            seats=data["seats"],
            prefix=data["code_prefix"],
        )
