import type { Meta, StoryObj } from "@storybook/svelte";

import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";

const meta: Meta<SectionLocationState> = {
    component: SectionLocationState,
    argTypes: {
        label: {
            control: {
                type: "text",
            },
        },
    },
};
export default meta;

type Story = StoryObj<SectionLocationState>;

export const Default: Story = {
    args: {
        label: "Section 1",
    },
};
