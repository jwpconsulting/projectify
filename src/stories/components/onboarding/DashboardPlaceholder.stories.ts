import type { Meta, StoryObj } from "@storybook/svelte";

import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";

const meta: Meta<DashboardPlaceholder> = {
    component: DashboardPlaceholder,
    argTypes: {},
};
export default meta;

type Story = StoryObj<DashboardPlaceholder>;

export const Default: Story = {};
