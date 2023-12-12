import type { Meta, StoryObj } from "@storybook/svelte";

import SubTaskLine from "$lib/figma/screens/task/SubTaskLine.svelte";
import { subTask } from "$lib/storybook";

const meta: Meta<SubTaskLine> = {
    component: SubTaskLine,
};
export default meta;

type Story = StoryObj<SubTaskLine>;

export const Default: Story = {
    args: {
        subTask,
    },
};
