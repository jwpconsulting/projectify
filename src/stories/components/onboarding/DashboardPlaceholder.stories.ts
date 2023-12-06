import type { Meta, StoryObj } from "@storybook/svelte";

import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";

const state = {
    kind: "new-workspace",
    title: "Hello world",
};

const meta: Meta<DashboardPlaceholder> = {
    component: DashboardPlaceholder,
    args: { state },
};
export default meta;

type Story = StoryObj<DashboardPlaceholder>;

export const Default: Story = {};
