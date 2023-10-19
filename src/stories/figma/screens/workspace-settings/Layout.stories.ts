import type { Meta, StoryObj } from "@storybook/svelte";

import Layout from "$lib/figma/screens/workspace-settings/Layout.svelte";
import { workspace } from "$lib/storybook";

import { activeSetting } from "./config";

const meta: Meta<Layout> = {
    component: Layout,
    argTypes: {
        activeSetting,
    },
    args: { workspace, activeSetting: "index" },
};
export default meta;

type Story = StoryObj<Layout>;

export const Default: Story = {};
