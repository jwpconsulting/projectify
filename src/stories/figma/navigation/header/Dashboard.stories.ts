import type { Meta, StoryObj } from "@storybook/svelte";

import Dashboard from "$lib/figma/navigation/header/Dashboard.svelte";
import { mobileParameters, user1 } from "$lib/storybook";

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
