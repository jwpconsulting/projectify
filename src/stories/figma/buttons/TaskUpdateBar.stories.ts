import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
import { taskUpdateBarStates, taskUpdateBarKinds } from "$lib/figma/types";

const meta: Meta<TaskUpdateBar> = {
    component: TaskUpdateBar,
    argTypes: {
        kind: {
            control: "radio",
            options: taskUpdateBarKinds,
        },
        state: {
            control: "radio",
            options: taskUpdateBarStates,
        },
    },
};
export default meta;

type Story = StoryObj<TaskUpdateBar>;

export const Default: Story = {
    args: {
        kind: "desktop",
        state: "task",
    },
};

export const Mobile: Story = {
    args: {
        kind: "mobile",
        state: "task",
    },
};
