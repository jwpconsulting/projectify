import type { Meta, StoryObj } from "@storybook/svelte";

import TabBar from "$lib/figma/screens/workspace-settings/TabBar.svelte";
import { workspace } from "$lib/storybook";

import { activeSetting } from "./config";

const meta: Meta<TabBar> = {
    component: TabBar,
    argTypes: { activeSetting },
    args: { workspace, activeSetting: "index" },
};
export default meta;

type Story = StoryObj<TabBar>;

export const Default: Story = {};
