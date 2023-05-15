import type { Meta, StoryObj } from "@storybook/svelte";

import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";

import { mobileParameters, workspaceBoardSection } from "$lib/storybook";

const meta: Meta<SectionTitle> = {
    component: SectionTitle,
    argTypes: {
        open: {
            control: "boolean",
        },
    },
    args: {
        workspaceBoardSection,
        open: true,
    },
};
export default meta;

type Story = StoryObj<SectionTitle>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
