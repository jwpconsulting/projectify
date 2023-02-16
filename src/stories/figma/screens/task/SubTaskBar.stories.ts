import type { Meta, StoryObj } from "@storybook/svelte";

import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";

const meta: Meta<SubTaskBar> = {
    component: SubTaskBar,
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

type Story = StoryObj<SubTaskBar>;

export const Default: Story = {
    args: {
        progress: 50,
    },
};
