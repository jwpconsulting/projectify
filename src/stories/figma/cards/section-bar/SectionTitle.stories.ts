import type { Meta, StoryObj } from "@storybook/svelte";

import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";

import { workspaceBoardSection, mobileParameters } from "$lib/storybook";

const meta: Meta<SectionTitle> = {
    component: SectionTitle,
    argTypes: {
        open: {
            control: "boolean",
        },
        isLast: {
            control: "boolean",
        },
        isFirst: {
            control: "boolean",
        },
    },
    args: {
        section: workspaceBoardSection,
        open: true,
        isFirst: true,
        isLast: false,
    },
};
export default meta;

type Story = StoryObj<SectionTitle>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
