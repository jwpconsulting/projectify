import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace } from "$lib/storybook";

import { activeSetting } from "./config";

import Layout from "$lib/figma/screens/workspace-settings/Layout.svelte";

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
