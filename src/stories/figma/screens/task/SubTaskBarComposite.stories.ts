import type { Meta, StoryObj } from "@storybook/svelte";

import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
import { subTask } from "$lib/storybook";

const meta: Meta<SubTaskBarComposite> = {
    component: SubTaskBarComposite,
};
export default meta;

type Story = StoryObj<SubTaskBarComposite>;

export const Default: Story = {
    args: {
        subTasks: [subTask, subTask],
    },
};

export const Empty: Story = {
    args: {
        subTasks: [],
    },
};
