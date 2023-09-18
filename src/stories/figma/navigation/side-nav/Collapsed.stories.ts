import type { Meta, StoryObj } from "@storybook/svelte";

import {
    workspace,
    workspaceUserSearchModule,
    labelSearchModule,
} from "$lib/storybook";

import Collapsed from "$lib/figma/navigation/side-nav/Collapsed.svelte";

const meta: Meta<Collapsed> = {
    component: Collapsed,
    args: {
        workspace,
        workspaces: [workspace],
        workspaceUserSearchModule,
        labelSearchModule,
    },
};
export default meta;

type Story = StoryObj<Collapsed>;

export const Default: Story = {};
