import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import WorkspaceSettingsMembers from "$lib/figma/screens/workspace-settings/WorkspaceSettingsMembers.svelte";

const meta: Meta<WorkspaceSettingsMembers> = {
    component: WorkspaceSettingsMembers,
    args: { workspace },
};
export default meta;

type Story = StoryObj<WorkspaceSettingsMembers>;

export const Default: Story = {};
