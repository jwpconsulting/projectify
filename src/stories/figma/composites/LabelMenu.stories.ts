import type { Meta, StoryObj } from "@storybook/svelte";

import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";

import { labelSearchModule } from "$lib/storybook";

const meta: Meta<LabelMenu> = {
    component: LabelMenu,
    argTypes: {},
    args: { labelSearchModule },
};
export default meta;

type Story = StoryObj<LabelMenu>;

export const Default: Story = {};
