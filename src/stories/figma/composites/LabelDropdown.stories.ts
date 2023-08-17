import type { Meta, StoryObj } from "@storybook/svelte";

import { labelSearchModule } from "$lib/storybook";

import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";

const meta: Meta<LabelDropdown> = {
    component: LabelDropdown,
    argTypes: {},
    args: { labelSearchModule },
};
export default meta;

type Story = StoryObj<LabelDropdown>;

export const Default: Story = {};
