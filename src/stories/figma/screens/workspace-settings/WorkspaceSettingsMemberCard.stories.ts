import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceUser } from "$lib/storybook";

import WorkspaceSettingsMemberCard from "$lib/figma/screens/workspace-settings/WorkspaceSettingsMemberCard.svelte";

const meta: Meta<WorkspaceSettingsMemberCard> = {
    component: WorkspaceSettingsMemberCard,
    args: { workspaceUser },
};
export default meta;

type Story = StoryObj<WorkspaceSettingsMemberCard>;

export const Default: Story = {};
