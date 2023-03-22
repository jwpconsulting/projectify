import type { Meta, StoryObj } from "@storybook/svelte";

import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";

const meta: Meta<LabelDropdown> = {
    component: LabelDropdown,
    argTypes: {},
};
export default meta;

type Story = StoryObj<LabelDropdown>;

export const Default: Story = {};
