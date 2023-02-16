import type { Meta, StoryObj } from "@storybook/svelte";

import SubTaskProgressBar from "$lib/figma/screens/task/SubTaskProgressBar.svelte";

const meta: Meta<SubTaskProgressBar> = {
    component: SubTaskProgressBar,
    argTypes: {
        progress: {
            control: {
                type: "number",
                min: 0,
                max: 100,
                step: 10,
            },
        },
    },
};
export default meta;

type Story = StoryObj<SubTaskProgressBar>;

export const Default: Story = {
    args: {
        progress: 50,
    },
};
