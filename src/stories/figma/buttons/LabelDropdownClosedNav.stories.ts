import type { Meta, StoryObj } from "@storybook/svelte";

import LabelDropdownClosedNav from "$lib/figma/buttons/LabelDropdownClosedNav.svelte";

const meta: Meta<LabelDropdownClosedNav> = {
    component: LabelDropdownClosedNav,
};
export default meta;

type Story = StoryObj<LabelDropdownClosedNav>;

export const Default: Story = {};
