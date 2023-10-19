import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateTaskCard from "$lib/figma/screens/task/UpdateTaskCard.svelte";
import { mobileParameters, task, workspaceBoardSection } from "$lib/storybook";

const meta: Meta<UpdateTaskCard> = {
    component: UpdateTaskCard,
    args: {
        task,
        workspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<UpdateTaskCard>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: {
        ...mobileParameters,
    },
};
