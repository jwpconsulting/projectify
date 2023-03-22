import type { Meta, StoryObj } from "@storybook/svelte";

import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";

import { labelSearchModule } from "$lib/storybook";

const meta: Meta<LabelDropdown> = {
    component: LabelDropdown,
    argTypes: {},
    args: { labelSearchModule },
};
export default meta;

type Story = StoryObj<LabelDropdown>;

export const Default: Story = {};
