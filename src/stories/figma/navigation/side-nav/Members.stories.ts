import { writable, readable } from "svelte/store";
import type { Meta, StoryObj } from "@storybook/svelte";

import Members from "$lib/figma/navigation/side-nav/Members.svelte";

import { workspaceUser } from "$lib/storybook";

import type { WorkspaceUserSearchModule } from "$lib/types/stores";

const workspaceUserSearchModule: WorkspaceUserSearchModule = {
    select: () => {},
    deselect: () => {},
    selected: writable({ kind: "allWorkspaceUsers" }),
    tasksPerUser: readable({ unassigned: 0, assigned: new Map() }),
    search: writable(""),
    searchResults: readable([workspaceUser]),
};

const meta: Meta<Members> = {
    component: Members,
    argTypes: {},
    args: {
        workspaceUserSearchModule,
    },
};
export default meta;

type Story = StoryObj<Members>;

export const Default: Story = {};
