import type { Meta, StoryObj } from "@storybook/svelte";

import {
    makeStorybookSelect,
    task,
    workspaceBoard,
    workspaceBoardSection,
    workspaceUser,
} from "$lib/storybook";

import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";

const target = makeStorybookSelect({
    "Delete label": {
        kind: "deleteLabel" as const,
        label: { name: "This is a label", color: 0, uuid: "" },
    },
    "Delete member": {
        kind: "deleteMember" as const,
        workspaceUser,
    },
    "Delete section": {
        kind: "deleteSection" as const,
        workspaceBoardSection,
    },
    "Delete task": {
        kind: "deleteTask" as const,
        task,
    },
    "Delete selected tasks": {
        kind: "deleteSelectedTasks" as const,
        tasks: [task],
    },
    "Archive board": {
        kind: "archiveBoard" as const,
        workspaceBoard: {
            title: "board name",
            created: "",
            modified: "",
            uuid: "",
        },
    },
    "Delete board": {
        kind: "deleteBoard" as const,
        workspaceBoard,
    },
});

const meta: Meta<DestructiveOverlay> = {
    component: DestructiveOverlay,
    argTypes: { target },
    args: { target: "delete-board" },
};
export default meta;

type Story = StoryObj<DestructiveOverlay>;

export const Default: Story = {};
