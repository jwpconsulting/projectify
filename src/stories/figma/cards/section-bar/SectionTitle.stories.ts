import type { Meta, StoryObj } from "@storybook/svelte";

import {
    mobileParameters,
    workspaceBoard,
    workspaceBoardSection,
} from "$lib/storybook";

import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";

const meta: Meta<SectionTitle> = {
    component: SectionTitle,
    argTypes: {
        open: {
            control: "boolean",
        },
    },
    args: {
        workspaceBoard,
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
