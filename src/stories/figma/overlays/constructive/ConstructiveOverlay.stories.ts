import type { Meta, StoryObj } from "@storybook/svelte";

import {
    makeStorybookSelect,
    workspace,
    workspaceBoard,
} from "$lib/storybook";

import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";

const target = makeStorybookSelect({
    "Update workspace board": { kind: "updateWorkspaceBoard", workspaceBoard },
    "Create workspace board": { kind: "createWorkspaceBoard", workspace },
    "Invite team members": { kind: "inviteTeamMembers", workspace },
    "Invite team members (no seats left": {
        kind: "inviteTeamMembersNoSeatsLeft",
        workspace,
    },
    "Create workspace board section": {
        kind: "createWorkspaceBoardSection",
        workspaceBoard,
    },
    "Create workspace": { kind: "createWorkspace" },
    "Skip onboarding": { kind: "skipOnboarding" },
    "Recover workspace board": {
        kind: "recoverWorkspaceBoard",
        workspaceBoard,
    },
});

const meta: Meta<ConstructiveOverlay> = {
    component: ConstructiveOverlay,
    argTypes: {
        target,
    },
    args: {
        target: "update-workspace-board",
    },
};
export default meta;

type Story = StoryObj<ConstructiveOverlay>;

export const Default: Story = {};
