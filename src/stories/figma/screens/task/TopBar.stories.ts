import type { Meta, StoryObj } from "@storybook/svelte";

import { createTaskModule, newTask } from "$lib/storybook";

import TopBar from "$lib/figma/screens/task/TopBar.svelte";

const meta: Meta<TopBar> = {
    component: TopBar,
    argTypes: {},
    args: {
        taskModule: createTaskModule,
        taskOrNewTask: { kind: "newTask", newTask },
    },
};
export default meta;

type Story = StoryObj<TopBar>;

export const Default: Story = {};
