import type { Meta, StoryObj } from "@storybook/svelte";

import { workspaceBoardSection } from "$lib/storybook";

import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";

const meta: Meta<TaskSection> = {
    component: TaskSection,
    args: { workspaceBoardSection },
};
export default meta;

type Story = StoryObj<TaskSection>;

export const Default: Story = {};
