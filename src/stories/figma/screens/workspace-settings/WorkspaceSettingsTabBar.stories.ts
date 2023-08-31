import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import { activeSetting } from "./config";

import WorkspaceSettingsTabBar from "$lib/figma/screens/workspace-settings/WorkspaceSettingsTabBar.svelte";

const meta: Meta<WorkspaceSettingsTabBar> = {
    component: WorkspaceSettingsTabBar,
    argTypes: { activeSetting },
    args: { workspace, activeSetting: "index" },
};
export default meta;

type Story = StoryObj<WorkspaceSettingsTabBar>;

export const Default: Story = {};
