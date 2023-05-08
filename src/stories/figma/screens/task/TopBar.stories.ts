import type { Meta, StoryObj } from "@storybook/svelte";

import TopBar from "$lib/figma/screens/task/TopBar.svelte";

import { createTaskModule, newTask } from "$lib/storybook";

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
