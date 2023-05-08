import type { Meta, StoryObj } from "@storybook/svelte";

import SubTask from "$lib/figma/buttons/SubTask.svelte";

import { subTaskStates } from "$lib/figma/types";

import { subTask } from "$lib/storybook";

const meta: Meta<SubTask> = {
    component: SubTask,
    argTypes: {
        state: {
            control: "inline-radio",
            options: subTaskStates,
        },
    },
};
export default meta;

type Story = StoryObj<SubTask>;

export const Default: Story = {
    args: {
        createOrUpdateSubTask: { kind: "update", update: subTask },
        state: "normal",
    },
};

export const Edit: Story = {
    args: {
        createOrUpdateSubTask: { kind: "update", update: subTask },
        state: "edit",
    },
};
