import type { Meta, StoryObj } from "@storybook/svelte";

import Billing from "$lib/figma/screens/workspace-settings/Billing.svelte";
import { workspace, customer } from "$lib/storybook";

const meta: Meta<Billing> = {
    component: Billing,
    args: { workspace, customer },
};
export default meta;

type Story = StoryObj<Billing>;

export const Default: Story = {};
