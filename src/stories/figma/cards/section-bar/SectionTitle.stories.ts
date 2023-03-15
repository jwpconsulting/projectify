import type { Meta, StoryObj } from "@storybook/svelte";

import SectionTitle from "$lib/figma/cards/section-bar/SectionTitle.svelte";

import { workspaceBoardSection } from "$lib/storybook";

const meta: Meta<SectionTitle> = {
    component: SectionTitle,
    argTypes: {},
    args: {
        section: workspaceBoardSection,
    },
};
export default meta;

type Story = StoryObj<SectionTitle>;

export const Default: Story = {};
