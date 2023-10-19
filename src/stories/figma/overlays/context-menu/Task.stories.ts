import type { Meta, StoryObj } from "@storybook/svelte";

import Task from "$lib/figma/overlays/context-menu/Task.svelte";
import { task } from "$lib/storybook";

const meta: Meta<Task> = {
    component: Task,
    argTypes: {},
    args: { task },
};
export default meta;

type Story = StoryObj<Task>;

export const Default: Story = {};
