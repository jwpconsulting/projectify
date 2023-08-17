import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters } from "$lib/storybook";

import Landing from "$lib/figma/navigation/header/Landing.svelte";

const meta: Meta<Landing> = {
    component: Landing,
    argTypes: {},
    args: {},
};
export default meta;

type Story = StoryObj<Landing>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
