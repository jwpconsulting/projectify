import type { Meta, StoryObj } from "@storybook/svelte";

import { mobileParameters, user1 } from "$lib/storybook";

import Dashboard from "$lib/figma/navigation/header/Dashboard.svelte";

const meta: Meta<Dashboard> = {
    component: Dashboard,
    argTypes: {},
    args: { user: user1 },
};
export default meta;

type Story = StoryObj<Dashboard>;

export const Desktop: Story = {};
export const Mobile: Story = {
    parameters: mobileParameters,
};
