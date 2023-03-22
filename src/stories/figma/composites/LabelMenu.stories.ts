import type { Meta, StoryObj } from "@storybook/svelte";

import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";

const meta: Meta<LabelMenu> = {
    component: LabelMenu,
    argTypes: {},
};
export default meta;

type Story = StoryObj<LabelMenu>;

export const Default: Story = {};
