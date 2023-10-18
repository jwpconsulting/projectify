import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import WorkspaceUsers from "$lib/figma/screens/workspace-settings/WorkspaceUsers.svelte";

const meta: Meta<WorkspaceUsers> = {
    component: WorkspaceUsers,
    args: { workspace },
};
export default meta;

type Story = StoryObj<WorkspaceUsers>;

export const Default: Story = {};
