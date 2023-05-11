import type { Meta, StoryObj } from "@storybook/svelte";

import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";
import { task } from "$lib/storybook";

const meta: Meta<TaskUpdateSection> = {
    component: TaskUpdateSection,
    args: { task },
};
export default meta;

type Story = StoryObj<TaskUpdateSection>;

export const Default: Story = {};
