"""Workspace schema subscription."""
import channels_graphql_ws
import graphene

from .. import (
    models,
)
from . import (
    types,
)


class OnWorkspaceChange(channels_graphql_ws.Subscription):
    """Notify on workspace changes."""

    class Arguments:
        """Arguments."""

        uuid = graphene.ID(required=True)

    workspace = graphene.Field(types.Workspace)

    @classmethod
    def subscribe(cls, root, info, uuid):
        """Return subscription information."""
        workspace = models.Workspace.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        return [str(workspace.uuid)]

    @classmethod
    def publish(cls, payload, info, uuid):
        """Publish subscription information."""
        return cls(payload)


class OnWorkspaceBoardChange(channels_graphql_ws.Subscription):
    """Notify ow workspace board changes."""

    class Arguments:
        """Arguments."""

        uuid = graphene.ID(required=True)

    workspace_board = graphene.Field(types.WorkspaceBoard)

    @classmethod
    def subscribe(cls, root, info, uuid):
        """Return subscription information."""
        workspace_board = models.WorkspaceBoard.objects.get_for_user_and_uuid(
            info.context.user,
            uuid,
        )
        return [str(workspace_board.uuid)]

    @classmethod
    def publish(cls, payload, info, uuid):
        """Publish subscription information."""
        return cls(payload)


class Subscription:
    """Subscription."""

    on_workspace_change = OnWorkspaceChange.Field()
    on_workspace_board_change = OnWorkspaceBoardChange.Field()
