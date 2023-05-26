import type { Meta, StoryObj } from "@storybook/svelte";

import Landing from "$lib/figma/navigation/header/Landing.svelte";
import { mobileParameters } from "$lib/storybook";

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
