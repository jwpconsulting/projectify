import type { Meta, StoryObj } from "@storybook/svelte";

import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
import { workspaceBoardSection } from "$lib/storybook";

const meta: Meta<TaskSection> = {
    component: TaskSection,
    args: { workspaceBoardSection },
};
export default meta;

type Story = StoryObj<TaskSection>;

export const Default: Story = {};
