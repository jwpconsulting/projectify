import type { Meta, StoryObj } from "@storybook/svelte";

import { workspace, customer } from "$lib/storybook";

import Billing from "$lib/figma/screens/workspace-settings/Billing.svelte";

const meta: Meta<Billing> = {
    component: Billing,
    args: { workspace, customer },
};
export default meta;

type Story = StoryObj<Billing>;

export const Default: Story = {};
