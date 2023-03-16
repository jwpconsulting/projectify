import type { Meta, StoryObj } from "@storybook/svelte";

import HelpButton from "$lib/figma/buttons/HelpButton.svelte";

const meta: Meta<HelpButton> = {
    component: HelpButton,
    argTypes: {},
};
export default meta;

type Story = StoryObj<HelpButton>;

export const Default: Story = {};
