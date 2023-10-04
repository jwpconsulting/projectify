import type { Meta, StoryObj } from "@storybook/svelte";

import UpdateSubTasks from "$lib/figma/screens/task/UpdateSubTasks.svelte";

const meta: Meta<UpdateSubTasks> = {
    component: UpdateSubTasks,
    argTypes: {},
};
export default meta;

type Story = StoryObj<UpdateSubTasks>;

export const Default: Story = {};
