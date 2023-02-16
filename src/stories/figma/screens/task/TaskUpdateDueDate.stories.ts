import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateDueDate from "$lib/figma/screens/task/TaskUpdateDueDate.svelte";

const meta: Meta<TaskUpdateDueDate> = {
    component: TaskUpdateDueDate,
    argTypes: {
        date: {
            control: {
                type: "radio",
            },
            options: [null, "2024-01-01"],
        },
    },
};
export default meta;

type Story = StoryObj<TaskUpdateDueDate>;

export const Default: Story = {
    args: { date: null },
};

export const DateSelected: Story = {
    args: { date: "2024-01-01" },
};

export const DueSoon: Story = {
    args: { date: "2024-01-01", dueSoon: true },
};
