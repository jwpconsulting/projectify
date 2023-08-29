import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoardSection } from "$lib/storybook";

import TaskUpdateSection from "$lib/figma/screens/task/TaskUpdateSection.svelte";

const meta: Meta<TaskUpdateSection> = {
    component: TaskUpdateSection,
    args: { workspaceBoardSection },
};
export default meta;

type Story = StoryObj<TaskUpdateSection>;

export const Default: Story = {};
