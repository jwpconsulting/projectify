import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceUsers from "$lib/figma/navigation/side-nav/WorkspaceUsers.svelte";

const meta: Meta<WorkspaceUsers> = {
    component: WorkspaceUsers,
};
export default meta;

type Story = StoryObj<WorkspaceUsers>;

export const Default: Story = {};
