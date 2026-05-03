# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Reusable forms for workspace app."""

from dataclasses import dataclass
from typing import Any, Optional

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model, QuerySet
from django.utils.translation import gettext_lazy as _

from projectify.workspace.models import TeamMember


@dataclass
class ModelMultipleChoice[T: Model]:
    """ModelMultipleChoiceField result."""

    selected_blank: bool
    selected_objects: Optional[QuerySet[T]]


class ModelMultipleChoiceFieldWithEmpty[T: Model](
    forms.ModelMultipleChoiceField
):
    """Override ModelMultipleChoiceField and allow empty label."""

    def __init__(self, queryset: QuerySet[Any], **kwargs: Any) -> None:
        """Override init."""
        super(forms.ModelMultipleChoiceField, self).__init__(
            queryset, **kwargs
        )

    def clean(self, value: list[str]) -> Optional[ModelMultipleChoice[T]]:
        """
        Return a tuple of values.

        The first value is a bool that tells you whether the user selected the blank
        option

        The second value is an optional queryset.
        If no values have been selected, it's empty. If values have been
        selected, it's a queryset.
        """
        has_empty = False
        value_without_empty: list[str] = []
        if len(value) == 0:
            return None
        for v in value:
            if len(v) == 0:
                has_empty = True
            else:
                value_without_empty.append(v)
        match value_without_empty:
            case []:
                cleaned = None
            case values:
                cleaned_qs: QuerySet[Any] = super().clean(values)
                if not cleaned_qs.exists():
                    cleaned = None
                else:
                    cleaned = cleaned_qs

        return ModelMultipleChoice(
            selected_blank=has_empty, selected_objects=cleaned
        )


class WorkspaceSearchForm(forms.Form):
    """Form for searching a workspace."""

    query = forms.CharField(
        label=_("Search workspace"),
        min_length=1,
        empty_value=None,
        widget=forms.TextInput(
            attrs={"type": "search", "placeholder": _("Search workspace")}
        ),
    )

    def __init__(
        self,
        team_members: Optional[QuerySet[TeamMember]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Populate choices."""
        super().__init__(*args, **kwargs)
        if team_members:
            member_widget = forms.CheckboxSelectMultiple()
            member_widget.option_template_name = (
                "workspace/forms/widgets/select_team_member_option.html"
            )
            self.fields["filter_by_team_member"] = (
                ModelMultipleChoiceFieldWithEmpty[
                    TeamMember
                ](
                    required=False,
                    blank=True,
                    label=_("Filter tasks by team member:"),
                    queryset=team_members,
                    widget=member_widget,
                    to_field_name="uuid",
                    empty_label=_("Assigned to nobody"),
                )
            )
            self.fields["query"].required = False

    def clean(self) -> dict[str, Any]:
        """Ensure that at least a query osdr team member filter is provided."""
        cleaned_data = super().clean()
        query = cleaned_data.get("query")
        filter_by_team_member = cleaned_data.get("filter_by_team_member")
        if query is None and filter_by_team_member is None:
            raise ValidationError(
                _(
                    "Please enter a search query or select at least one team member to filter by."
                )
            )
        return cleaned_data
