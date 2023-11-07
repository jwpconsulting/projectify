import type { Meta, StoryObj } from "@storybook/svelte";

import HelpSections from "$lib/components/help/HelpSections.svelte";

const meta: Meta<HelpSections> = {
    component: HelpSections,
    argTypes: {},
};
export default meta;

type Story = StoryObj<HelpSections>;

export const Default: Story = {};
