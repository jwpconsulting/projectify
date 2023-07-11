import type { Meta, StoryObj } from "@storybook/svelte";

import SectionBar from "$lib/figma/cards/SectionBar.svelte";

import {
    mobileParameters,
    workspaceBoard,
    workspaceBoardSection,
} from "$lib/storybook";

const meta: Meta<SectionBar> = {
    component: SectionBar,
    argTypes: {},
    args: {
        workspaceBoard,
        workspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<SectionBar>;

export const Default: Story = {};

export const Mobile: Story = {
    parameters: mobileParameters,
};
