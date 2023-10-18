import type { Meta, StoryObj } from "@storybook/svelte";

import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";

const meta: Meta<WorkspaceSettings> = {
    component: WorkspaceSettings,
    argTypes: {},
};
export default meta;

type Story = StoryObj<WorkspaceSettings>;

export const Default: Story = {};
