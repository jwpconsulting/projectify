import type { Meta, StoryObj } from "@storybook/svelte";

import TaskContextMenu from "$lib/figma/overlays/context-menu/TaskContextMenu.svelte";

import { task } from "$lib/storybook";

const meta: Meta<TaskContextMenu> = {
    component: TaskContextMenu,
    argTypes: {},
    args: { task },
};
export default meta;

type Story = StoryObj<TaskContextMenu>;

export const Default: Story = {};
