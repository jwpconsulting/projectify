import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateSubTasks from "$lib/figma/screens/task/UpdateSubTasks.svelte";
import { createSubTaskAssignment } from "$lib/stores/dashboard";

const meta: Meta<UpdateSubTasks> = {
    component: UpdateSubTasks,
    args: {
        subTaskAssignment: createSubTaskAssignment(),
    },
};
export default meta;

type Story = StoryObj<UpdateSubTasks>;

export const Default: Story = {};
