"""Corporate admin."""
from typing import Any, Optional

from django import forms
from django.contrib import (
    admin,
)
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from corporate.models.custom_code import CustomCode
from corporate.services.custom_code import custom_code_create
from user.models import User

from . import (
    models,
)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin[models.Customer]):
    """Customer Admin."""

    list_display = ("workspace_title", "seats", "subscription_status")
    list_select_related = ("workspace",)
    readonly_fields = (
        "uuid",
        "stripe_customer_id",
    )

    @admin.display(description=_("Workspace title"))
    def workspace_title(self, instance: models.Customer) -> str:
        """Return the workspace's title."""
        return instance.workspace.title


@admin.register(CustomCode)
class CustomCodeAdmin(admin.ModelAdmin[CustomCode]):
    """Customer Admin."""

    list_display = ("seats", "customer", "used", "code")
    readonly_fields = ("code",)
    list_select_related = ("customer",)

    class CustomCodeForm(forms.ModelForm):
        """Form for custom code creation."""

        seats = forms.IntegerField(min_value=1, initial=1)
        code_prefix = forms.CharField(min_length=5, max_length=50)

        class Meta:
            """Specify model."""

            fields = ("seats",)
            model = CustomCode

    def get_form(
        self,
        request: HttpRequest,
        obj: Optional[CustomCode] = None,
        change: bool = False,
        **kwargs: Any,
    ) -> type[forms.ModelForm]:
        """Return a custom form for creation, otherwise return regular."""
        if obj:
            return super().get_form(request, obj, change, **kwargs)  # type: ignore[no-any-return]
        return self.CustomCodeForm

    def save_model(
        self,
        request: HttpRequest,
        obj: CustomCode,
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
        custom_code_create(
            who=user,
            seats=data["seats"],
            prefix=data["code_prefix"],
        )
