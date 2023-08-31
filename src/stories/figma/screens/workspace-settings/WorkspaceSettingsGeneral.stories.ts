import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import WorkspaceSettingsGeneral from "$lib/figma/screens/workspace-settings/WorkspaceSettingsGeneral.svelte";

const meta: Meta<WorkspaceSettingsGeneral> = {
    component: WorkspaceSettingsGeneral,
    args: { workspace },
};
export default meta;

type Story = StoryObj<WorkspaceSettingsGeneral>;

export const Default: Story = {};
