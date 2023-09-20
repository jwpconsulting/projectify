import type { Meta, StoryObj } from "@storybook/svelte";

import { task } from "$lib/storybook";

import Task from "$lib/figma/overlays/context-menu/Task.svelte";

const meta: Meta<Task> = {
    component: Task,
    argTypes: {},
    args: { task },
};
export default meta;

type Story = StoryObj<Task>;

export const Default: Story = {};
