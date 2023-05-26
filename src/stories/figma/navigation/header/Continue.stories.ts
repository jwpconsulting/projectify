import type { Meta, StoryObj } from "@storybook/svelte";

import Continue from "$lib/figma/navigation/header/Continue.svelte";
import { mobileParameters } from "$lib/storybook";

const meta: Meta<Continue> = {
    component: Continue,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Continue>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
