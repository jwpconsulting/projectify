import type { Meta, StoryObj } from "@storybook/svelte";

import SectionBar from "$lib/figma/cards/SectionBar.svelte";

import { workspaceBoardSection } from "$lib/storybook";

const meta: Meta<SectionBar> = {
    component: SectionBar,
    argTypes: {
        isFirst: {
            control: "boolean",
        },
        isLast: {
            control: "boolean",
        },
    },
    args: {
        section: workspaceBoardSection,
        isFirst: true,
        isLast: false,
    },
};
export default meta;

type Story = StoryObj<SectionBar>;

export const Default: Story = {};
