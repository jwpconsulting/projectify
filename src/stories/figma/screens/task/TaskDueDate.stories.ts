import type { Meta, StoryObj } from "@storybook/svelte";

import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";

const meta: Meta<TaskDueDate> = {
    component: TaskDueDate,
    args: { readonly: false },
    argTypes: {
        readonly: { control: "boolean" },
        date: {
            control: {
                type: "radio",
            },
            options: [null, "2024-01-01", "2024-01-01T23:23"],
        },
    },
};
export default meta;

type Story = StoryObj<TaskDueDate>;

export const Default: Story = {
    args: { date: null },
};

export const DateSelected: Story = {
    args: { date: "2024-01-01" },
};

export const DueSoon: Story = {
    args: { date: "2024-01-01", dueSoon: true },
};
