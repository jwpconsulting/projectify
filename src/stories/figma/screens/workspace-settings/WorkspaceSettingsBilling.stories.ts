import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import WorkspaceSettingsBilling from "$lib/figma/screens/workspace-settings/WorkspaceSettingsBilling.svelte";

const meta: Meta<WorkspaceSettingsBilling> = {
    component: WorkspaceSettingsBilling,
    args: { workspace },
};
export default meta;

type Story = StoryObj<WorkspaceSettingsBilling>;

export const Default: Story = {};
