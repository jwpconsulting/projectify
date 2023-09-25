"""Label manager and model."""
import uuid
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Self,
    cast,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _

from .types import (
    Pks,
)
from .workspace import Workspace as Workspace


# TODO Here we could be using __all__


class LabelQuerySet(models.QuerySet["Label"]):
    """Label Queryset."""

    def filter_by_workspace_pks(self, workspace_pks: Pks) -> Self:
        """Filter by workspace pks."""
        return self.filter(workspace__pk__in=workspace_pks)

    def filter_for_user_and_uuid(
        self, user: AbstractBaseUser, uuid: uuid.UUID
    ) -> Self:
        """Return for matching workspace user and uuid."""
        return self.filter(workspace__users=user, uuid=uuid)


class Label(models.Model):
    """A label."""

    name = models.CharField(max_length=255)
    color = models.PositiveBigIntegerField(
        help_text=_("Color index"),
        default=0,
    )
    workspace = models.ForeignKey[Workspace](
        Workspace,
        on_delete=models.CASCADE,
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    objects: ClassVar[LabelQuerySet] = cast(  # type: ignore[assignment]
        LabelQuerySet, LabelQuerySet.as_manager()
    )

    if TYPE_CHECKING:
        id: int

    class Meta:
        """Meta."""

        unique_together = ("workspace", "name")
